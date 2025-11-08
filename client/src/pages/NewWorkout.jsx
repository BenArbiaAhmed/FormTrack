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
import { useState } from "react"
import * as z from "zod"; 
import { datetime } from "zod/v4/core/regexes.cjs"
 
const Exercise = z.object({ 
    name: z.string(),
    repetitions: z.number(),
    partial_reps: z.number()
});

const Workout = z.object({ 
    started_at: z.iso.datetime(),
    exercises: z.array(Exercise)
});





export default function NewWorkout() {
  const [currentExercise, setCurrentExercise] = useState(null)
  const [workoutStatus, setWorkoutStatus] = useState("stopped")
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [newWorout, setNewWorkout] = useState({})

  const handleStart = () => {
    if (!currentExercise) {
      return
    }
    setNewWorkout({
        started_at: new datetime(),
        exercises: []
    })
    setWorkoutStatus("running")
    setIsDialogOpen(false)
  }

  const handleStop = () => {
    setWorkoutStatus("stopped")
    setCurrentExercise(null)
  }

  return (
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
              {workoutStatus === "running" && (
                <img 
                  src={`http://localhost:8000/video/${currentExercise}`} 
                  alt="Video feed"
                  className="w-full max-w-[1280px] h-auto aspect-video"
                />
              )}

              {(workoutStatus === "running" || workoutStatus === "paused") && (
                <div className="flex flex-col p-1 gap-1">
                    <Button variant="outline" onClick={handleStop}>End</Button>
                    <Select 
                      value={currentExercise} 
                      onValueChange={setCurrentExercise}
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
                        <SelectItem value="triceps-dip">Triceps Dip</SelectItem>
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
  )
}