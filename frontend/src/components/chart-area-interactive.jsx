"use client"

import * as React from "react"
import { useEffect, useState, useMemo } from "react"
import { Area, AreaChart, CartesianGrid, XAxis } from "recharts"

import { useIsMobile } from "@/hooks/use-mobile"
import {
  Card,
  CardAction,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import {
  ToggleGroup,
  ToggleGroupItem,
} from "@/components/ui/toggle-group"

export const description = "An interactive area chart"


const chartConfig = {
  visitors: {
    label: "duration",
  },
  desktop: {
    label: "squat",
    color: "var(--primary)",
  },
  mobile: {
    label: "pushup",
    color: "var(--primary)",
  },
}

export function ChartAreaInteractive({ fetchedData }) {
  const isMobile = useIsMobile()
  const [timeRange, setTimeRange] = useState("90d")
  const [chartData, setChartData] = useState([])
  const [exerciseNames, setExerciseNames] = useState([])

  useEffect(() => {
    if (isMobile) {
      setTimeRange("7d")
    }
  }, [isMobile])

  useEffect(() => {
    if (!fetchedData || fetchedData.length === 0) return;
    
    try {
      const exercises = new Set();
      fetchedData.forEach(workout => {
        workout.exercises.forEach(exercise => {
          exercises.add(exercise.name);
        });
      });
      
      setExerciseNames(Array.from(exercises));
      setChartData(formatWorkoutsForChart(fetchedData));  
    } catch (error) {
      console.error(error);
    }
  }, [fetchedData])

  const filteredData = useMemo(() => {
    return chartData.filter((item) => {
      const date = new Date(item.date)
      const referenceDate = new Date().toISOString().split('T')[0]
      let daysToSubtract = 90
      if (timeRange === "30d") {
        daysToSubtract = 30
      } else if (timeRange === "7d") {
        daysToSubtract = 7
      }
      const startDate = new Date(referenceDate)
      startDate.setDate(startDate.getDate() - daysToSubtract)
      return date >= startDate
    })
  }, [chartData, timeRange])

  function formatWorkoutsForChart(workouts, metric = 'repetitions') {
    const exerciseNames = new Set();
    workouts.forEach(workout => {
      workout.exercises.forEach(exercise => {
        exerciseNames.add(exercise.name);
      });
    });
    
    return workouts.map(workout => {
      const dataPoint = {
        date: workout.started_at.split('T')[0]
      };

      exerciseNames.forEach(name => {
        dataPoint[name] = 0;
      });

      workout.exercises.forEach(exercise => {
        if (metric === 'repetitions') {
          dataPoint[exercise.name] = exercise.repetitions + (exercise.partial_reps || 0);
        } else if (metric === 'duration') {
          dataPoint[exercise.name] = exercise.duration;
        }
      });

      return dataPoint;
    });
  }


  const colors = ['hsl(var(--chart-1))', 'hsl(var(--chart-2))', 'hsl(var(--chart-3))', 'hsl(var(--chart-4))', 'hsl(var(--chart-5))'];

  return (
    <Card className="@container/card">
      <CardHeader>
        <CardTitle>Total Repetitions</CardTitle>
        <CardDescription>
          <span className="hidden @[540px]/card:block">
            Total for the last 3 months
          </span>
          <span className="@[540px]/card:hidden">Last 3 months</span>
        </CardDescription>
        <CardAction>
          <ToggleGroup
            type="single"
            value={timeRange}
            onValueChange={(value) => {
              console.log('Toggle clicked, new value:', value);
              setTimeRange(value);
            }}
            variant="outline"
            className="*:data-[slot=toggle-group-item]:px-4! @[767px]/card:flex"
          >
            <ToggleGroupItem value="90d">Last 3 months</ToggleGroupItem>
            <ToggleGroupItem value="30d">Last 30 days</ToggleGroupItem>
            <ToggleGroupItem value="7d">Last 7 days</ToggleGroupItem>
          </ToggleGroup>
          <Select value={timeRange} onValueChange={setTimeRange}>
            <SelectTrigger
              className="flex w-40 **:data-[slot=select-value]:block **:data-[slot=select-value]:truncate @[767px]/card:hidden"
              size="sm"
              aria-label="Select a value"
            >
              <SelectValue placeholder="Last 3 months" />
            </SelectTrigger>
            <SelectContent className="rounded-xl">
              <SelectItem value="90d" className="rounded-lg">
                Last 3 months
              </SelectItem>
              <SelectItem value="30d" className="rounded-lg">
                Last 30 days
              </SelectItem>
              <SelectItem value="7d" className="rounded-lg">
                Last 7 days
              </SelectItem>
            </SelectContent>
          </Select>
        </CardAction>
      </CardHeader>
      <CardContent className="px-2 pt-4 sm:px-6 sm:pt-6">
        <ChartContainer
          config={chartConfig}
          className="aspect-auto h-[250px] w-full"
        >
          <AreaChart data={filteredData}>
            <defs>
              {exerciseNames.map((exercise, index) => (
                <linearGradient key={exercise} id={`fill${exercise}`} x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor={colors[index % colors.length]}
                    stopOpacity={0.8}
                  />
                  <stop
                    offset="95%"
                    stopColor={colors[index % colors.length]}
                    stopOpacity={0.1}
                  />
                </linearGradient>
              ))}
            </defs>
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="date"
              tickLine={false}
              axisLine={false}
              tickMargin={8}
              minTickGap={32}
              tickFormatter={(value) => {
                const date = new Date(value)
                return date.toLocaleDateString("en-US", {
                  month: "short",
                  day: "numeric",
                })
              }}
            />
            <ChartTooltip
              cursor={false}
              content={
                <ChartTooltipContent
                  labelFormatter={(value) => {
                    return new Date(value).toLocaleDateString("en-US", {
                      month: "short",
                      day: "numeric",
                    })
                  }}
                  indicator="dot"
                />
              }
            />
            {exerciseNames.map((exercise, index) => (
              <Area
                key={exercise}
                dataKey={exercise}
                type="natural"
                fill={`url(#fill${exercise})`}
                stroke={colors[index % colors.length]}
                stackId="a"
              />
            ))}
          </AreaChart>
        </ChartContainer>
      </CardContent>
    </Card>
  )
}
