"use client"

import { IconCirclePlusFilled, IconMail } from "@tabler/icons-react"
import { Link } from "react-router-dom"
import { Button } from "@/components/ui/button"
import { NavLink } from "react-router-dom"
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar"

export function NavMain({
  items,
}) {
  return (
    <SidebarGroup>
      <SidebarGroupContent className="flex flex-col gap-2">
        <SidebarMenu>
          <Link to="/train">
          <SidebarMenuItem className="flex items-center gap-2 ">
            <SidebarMenuButton
              tooltip="Quick Create"
              className="bg-primary text-primary-foreground hover:bg-primary/90 hover:text-primary-foreground active:bg-primary/90 active:text-primary-foreground min-w-8 duration-200 ease-linear cursor-pointer"
            >
              <IconCirclePlusFilled />
              
                <span>Start new workout</span>
              
            </SidebarMenuButton>
          </SidebarMenuItem>
          </Link>
        </SidebarMenu>
        <SidebarMenu>
          {items.map((item) => (
            <SidebarMenuItem key={item.title}>
              <NavLink
                to={`/${item.title.toLowerCase()}`}
                className={({ isActive, isPending }) =>
                  isPending ? "pending" : isActive ? "text-red-500" : ""
                }
              >
                {({ isActive, isPending }) => (
                  <SidebarMenuButton tooltip={item.title} isActive={isActive} className="data-[active=true]:bg-gray-300" >
                    {item.icon && <item.icon />}
                    <span>{item.title}</span>
                  </SidebarMenuButton>
                )}
              </NavLink>
              
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}
