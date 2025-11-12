import { AppSidebar } from "@/components/app-sidebar"
import { ChartAreaInteractive } from "@/components/chart-area-interactive"
import { SectionCards } from "@/components/section-cards"
import { SiteHeader } from "@/components/site-header"
import {
  SidebarInset,
  SidebarProvider,
} from "@/components/ui/sidebar"
import axios from '../axios/axiosInstance'
import { useEffect, useState } from "react"
import DataTable from "../components/table"

import { Toaster } from "react-hot-toast"

export default function WorkoutsPage() {
  const [fetchedWorkoutsData, setFetchedWorkoutsData] = useState([])

  async function getDashboardData() {
    try {
        const response = await axios.get('/workout');
        const workoutsData = response.data;
        setFetchedWorkoutsData(workoutsData); 
      } catch (error) {
        console.error(error);
      }
  }
  
  useEffect(()=>{
    getDashboardData()
  }, [])
  
  return (
    <>
    <div><Toaster/></div>
    
    <SidebarProvider
      style={
        {
          "--sidebar-width": "calc(var(--spacing) * 72)",
          "--header-height": "calc(var(--spacing) * 12)",
        } 
      }
    >
      <AppSidebar variant="inset" />
      <SidebarInset>
        <SiteHeader />
        <div className="flex flex-1 flex-col">
          <div className="@container/main flex flex-1 flex-col gap-2">
            <div className="flex flex-col gap-4 py-4 md:gap-6 md:py-4">
              <DataTable fetchedData={fetchedWorkoutsData}  />
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
    </>
  )
}
