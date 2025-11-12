import { IconTrendingDown, IconTrendingUp } from "@tabler/icons-react"

import { Badge } from "@/components/ui/badge"
import {
  Card,
  CardAction,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import { useEffect, useState } from "react"

export function SectionCards( { fetchedData } ) {
  const[totalWorkoutsDuration, setTotalWorkoutsDuration] = useState(0)
  const[totalSquatCount, setTotalSquatCount] = useState(0)
  const[totalPushupCount, setTotalPushupCount] = useState(0)
  const[totalTricepsDipCount, setTotalTricepsDipCount] = useState(0)

  const populateCards = () =>{
    let totalDuration = 0;
    let totalSquatReps = 0;
    let totalPushupReps = 0;
    let totalTricepDipReps = 0;
    fetchedData.forEach(workout => {
    totalDuration += workout.duration;

    workout.exercises.forEach(exercise => {
      switch(exercise.name) {
        case 'squat':
          totalSquatReps += exercise.repetitions;
          break;
        case 'pushup':
          totalPushupReps += exercise.repetitions;
          break;
        case 'tricep_dip':
          totalTricepDipReps += exercise.repetitions;
          break;
      }
    });


    setTotalWorkoutsDuration(totalDuration)
    setTotalSquatCount(totalSquatReps)
    setTotalPushupCount(totalPushupReps)
    setTotalTricepsDipCount(totalTricepDipReps)
  });
  }

  useEffect(()=>{
    console.log(fetchedData)
    populateCards()
  },[fetchedData])

  return (
    <div className="*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card dark:*:data-[slot=card]:bg-card grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:bg-linear-to-t *:data-[slot=card]:shadow-xs lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Total Workouts Duration</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            {totalWorkoutsDuration} m
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingUp />
            </Badge>
          </CardAction>
        </CardHeader>
      </Card>
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Total Squat Count</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            {totalSquatCount}
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingDown />
            </Badge>
          </CardAction>
        </CardHeader>
      </Card>
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Total Pushup Count</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            {totalPushupCount}
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingUp />
            </Badge>
          </CardAction>
        </CardHeader>
      </Card>
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Total Triceps Dip Count</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            {totalTricepsDipCount}
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingUp />
            </Badge>
          </CardAction>
        </CardHeader>
      </Card>
    </div>
  )
}
