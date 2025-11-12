import { AppSidebar } from "@/components/app-sidebar"
import { SiteHeader } from "@/components/site-header"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogClose,
  DialogFooter
} from "@/components/ui/dialog"

import { Button } from "@/components/ui/button"

import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { useState, useRef, useEffect } from "react"
import { z } from 'zod';
import axios from '../axios/axiosInstance'
import toast, { Toaster } from "react-hot-toast"
 
const Exercise = z.object({ 
    name: z.string(),
    repetitions: z.number(),
    partial_reps: z.number()
});

const Workout = z.object({ 
    started_at: z.string().datetime(),
    exercises: z.array(Exercise)
});

export default function NewWorkout() {
  const [currentExercise, setCurrentExercise] = useState("")
  const [workoutStatus, setWorkoutStatus] = useState("stopped")
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [newWorkout, setNewWorkout] = useState({})
  const [repCount, setRepCount] = useState({ reps: 0, partial_reps: 0 })
  const [sessionId, setSessionId] = useState(null)
  const eventSourceRef = useRef(null)
  const [exerciseStartTime, setExerciseStartTime] = useState(null)

  useEffect(() => {
    return () => {
      eventSourceRef.current?.close()
    }
  }, [sessionId])

  useEffect(() => {
    if (workoutStatus === "running" && sessionId) {
      eventSourceRef.current = new EventSource(
        `http://localhost:8000/api/v1/session/rep-count/${sessionId}`
      )

      eventSourceRef.current.onmessage = (event) => {
        const data = JSON.parse(event.data)
        setRepCount(data)
      }

      eventSourceRef.current.onerror = (error) => {
        console.error("SSE Error:", error)
        eventSourceRef.current?.close()
      }

      return () => {
        eventSourceRef.current?.close()
      }
    }
  }, [workoutStatus, sessionId])

  const handleStart = async () => {
    if (!currentExercise) return
    
    const newSessionId = crypto.randomUUID()
    
    try {
      await axios.post(`/session/start-session/${newSessionId}/${currentExercise}`);      
      setSessionId(newSessionId)
      setExerciseStartTime(new Date())
      setNewWorkout({
        started_at: new Date().toISOString(),
        exercises: []
      })
      setWorkoutStatus("running")
      setIsDialogOpen(false)
    } catch (error) {
      console.error('Error starting session:', error)
      throw new Error('Failed to start session')
      
    }
  }

  const handleStop = async () => {
    if (!sessionId) return
    
    try {
      const response = await axios.post(`/session/end-session/${sessionId}`); 
      setSessionId(null)
      const data = response.data
      const exerciseDuration = exerciseStartTime 
      ? Math.floor((new Date() - exerciseStartTime) / 60000) 
      : 0
      setNewWorkout(prev => ({
      ...prev,
      exercises: [
        ...prev.exercises,
        {
          name: currentExercise,
          repetitions: data.final_counts.reps,
          partial_reps: data.final_counts.partial_reps,
          duration: exerciseDuration
        }
      ]
    }))
    const workoutToSave = {
      ...newWorkout,
      exercises: [
        ...newWorkout.exercises,
        {
          name: currentExercise,
          repetitions: data.final_counts.reps,
          partial_reps: data.final_counts.partial_reps,
          duration: exerciseDuration
        }
      ]
    }
    return workoutToSave
    } catch (error) {
      console.error('Error ending session:', error)
    } finally {
      eventSourceRef.current?.close()
      
      setWorkoutStatus("stopped")
      setCurrentExercise("")
      setRepCount({ reps: 0, partial_reps: 0 })
      setSessionId(null)
      setExerciseStartTime(null)
    }
  }

  const handleExerciseChange = async (value) => {
    await handleStop()
    
    setCurrentExercise(value)
    
    const newSessionId = crypto.randomUUID()
    
    try {
      await axios.post(`/session/start-session/${newSessionId}/${value}`);
      setSessionId(newSessionId)
      setExerciseStartTime(new Date())
      setWorkoutStatus("running")
    } catch (error) {
      console.error('Error starting new exercise:', error)
    }
  }

  const handleSaveWorkout = async () => {
    let workoutToSave = await handleStop()
    
    const endTime = new Date()
    const startTime = new Date(workoutToSave.started_at)
    const totalDuration = Math.floor((endTime - startTime) / 60000)
    
    try {
      const workoutToSaveData = {
        ...workoutToSave,
        duration: totalDuration, 
      }
      console.log(workoutToSaveData)
      const response = await axios.post('/workout/new', workoutToSaveData)
      console.log(response)
      toast.success("Successfully saved new workout !")
    } catch (error) {
      toast.success("Failed to saved new workout")
      console.error(error)
    }
  }

  return (
    <>
    
    <div><Toaster/></div>
    <SidebarProvider
      style={{
        "--sidebar-width": "calc(var(--spacing) * 72)",
        "--header-height": "calc(var(--spacing) * 12)",
      }}
    >
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-6 items-center">
              {workoutStatus === "running" && sessionId && (
                <img 
                  src={`http://localhost:8000/api/v1/session/video/${sessionId}/${currentExercise}`} 
                  alt="Video feed"
                  className="w-full max-w-7xl h-auto aspect-video"
                />
              )}

              {(workoutStatus === "running" || workoutStatus === "paused") && (
                <div className="flex flex-col p-1 gap-1">
                    <Button variant="outline" onClick={handleSaveWorkout}>Save Workout</Button>
                    <Button variant="outline" onClick={handleStop}>Discard</Button>
                    <Select 
                      value={currentExercise} 
                      onValueChange={handleExerciseChange}
                    >
                        Change Exercise:
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Select an exercise" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pushup">Pushup</SelectItem>
                        <SelectItem value="squat">Squat</SelectItem>
                        <SelectItem value="tricep_dip">Triceps Dip</SelectItem>
                      </SelectContent>
                    </Select>
                </div>
                    
              )}

              {(workoutStatus === "stopped" || workoutStatus === "paused") && (
                <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
                  <DialogTrigger asChild>
                    <Button>Start Workout</Button>
                  </DialogTrigger>
                  <DialogContent>
                    <DialogHeader>
                      <DialogTitle>Let's start</DialogTitle>
                      <DialogDescription>
                        Choose your first exercise to start with:
                      </DialogDescription>
                    </DialogHeader>
                    
                    <Select 
                      value={currentExercise} 
                      onValueChange={setCurrentExercise}
                    >
                      <SelectTrigger className="w-full">
                        <SelectValue placeholder="Select an exercise" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="pushup">Pushup</SelectItem>
                        <SelectItem value="squat">Squat</SelectItem>
                        <SelectItem value="tricep_dip">Triceps Dip</SelectItem>
                      </SelectContent>
                    </Select>

                    <DialogFooter>
                      <DialogClose asChild>
                        <Button variant="outline">Cancel</Button>
                      </DialogClose>
                      <Button 
                        onClick={handleStart}
                        disabled={!currentExercise}
                      >
                        Start
                      </Button>
                    </DialogFooter>
                  </DialogContent>
                </Dialog>
              )}
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
    </>
  )
}