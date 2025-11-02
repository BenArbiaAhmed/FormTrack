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
    populateCards()
  },[])

  return (
    <div className="*:data-[slot=card]:from-primary/5 *:data-[slot=card]:to-card dark:*:data-[slot=card]:bg-card grid grid-cols-1 gap-4 px-4 *:data-[slot=card]:bg-gradient-to-t *:data-[slot=card]:shadow-xs lg:px-6 @xl/main:grid-cols-2 @5xl/main:grid-cols-4">
      <Card className="@container/card">
        <CardHeader>
          <CardDescription>Total Workouts Duration</CardDescription>
          <CardTitle className="text-2xl font-semibold tabular-nums @[250px]/card:text-3xl">
            {totalWorkoutsDuration} m
          </CardTitle>
          <CardAction>
            <Badge variant="outline">
              <IconTrendingUp />
              {/* +12.5% */}
            </Badge>
          </CardAction>
        </CardHeader>
        {/* <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">
            Trending up this month <IconTrendingUp className="size-4" />
          </div>
          <div className="text-muted-foreground">
            Visitors for the last 6 months
          </div>
        </CardFooter> */}
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
              {/* -20% */}
            </Badge>
          </CardAction>
        </CardHeader>
        {/* <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">
            Down 20% this period <IconTrendingDown className="size-4" />
          </div>
          <div className="text-muted-foreground">
            Acquisition needs attention
          </div>
        </CardFooter> */}
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
              {/* +12.5% */}
            </Badge>
          </CardAction>
        </CardHeader>
        {/* <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">
            Strong user retention <IconTrendingUp className="size-4" />
          </div>
          <div className="text-muted-foreground">Engagement exceed targets</div>
        </CardFooter> */}
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
              {/* +4.5% */}
            </Badge>
          </CardAction>
        </CardHeader>
        {/* <CardFooter className="flex-col items-start gap-1.5 text-sm">
          <div className="line-clamp-1 flex gap-2 font-medium">
            Steady performance increase <IconTrendingUp className="size-4" />
          </div>
          <div className="text-muted-foreground">Meets growth projections</div>
        </CardFooter> */}
      </Card>
    </div>
  )
}
