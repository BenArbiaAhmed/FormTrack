import { useState, useEffect, useRef, useCallback } from 'react'
import './App.css'

function App() {


  return (
    <>
    <div className="video-container">
        <img
          src="http://localhost:8000/video"
          alt="Video Stream"
          className="video-stream"
        />
      </div>
    </>
  )
}

export default App