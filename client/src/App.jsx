import { useState, useEffect, useRef, useCallback } from 'react'
import './App.css'
import Webcam from "react-webcam";

function App() {
  const [text, setText] = useState("")
  const [messages, setMessages] = useState([])
  const [ws, setWs] = useState(null)
  const [imageSrc, setImageSrc] = useState(null)
  const intervalRef = useRef(null);
  const webcamRef = useRef(null);
  
  const videoConstraints = {
    width: 1280,
    height: 720,
    facingMode: "user"
  };

  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/ws");
    
    websocket.onmessage = function(event) {
      setMessages(prev => [...prev, event.data])
    };

    websocket.onopen = () => {
      console.log("WebSocket connected")
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error)
    };

    setWs(websocket)

    return () => {
      websocket.close()
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [])


  const capture = useCallback(() => {
    if (webcamRef.current) {
      const screenshot = webcamRef.current.getScreenshot();
      setImageSrc(screenshot);
      console.log(screenshot);
    }
  }, [webcamRef]);

  const start = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
    }
    intervalRef.current = setInterval(capture, 100);
  }

  const stop = () => {
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  }

  return (
    <>
      <Webcam
        audio={false}
        height={720}
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={1280}
        videoConstraints={videoConstraints}
      />
      <button onClick={start}>Start</button>
      <button onClick={stop}>Stop</button>
    </>
  )
}

export default App