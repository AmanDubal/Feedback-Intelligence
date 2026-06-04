import * as React from "react"
import { cn } from "@/lib/utils"

const ChartContainer = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn(
        "flex flex-col gap-4 rounded-lg border border-slate-200 bg-white p-6 dark:border-slate-800 dark:bg-slate-950",
        className
      )}
      {...props}
    />
  )
)
ChartContainer.displayName = "ChartContainer"

const ChartTitle = React.forwardRef<HTMLHeadingElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3
      ref={ref}
      className={cn(
        "text-lg font-semibold leading-none tracking-tight text-slate-950 dark:text-slate-50",
        className
      )}
      {...props}
    />
  )
)
ChartTitle.displayName = "ChartTitle"

const ChartDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-slate-500 dark:text-slate-400", className)}
    {...props}
  />
))
ChartDescription.displayName = "ChartDescription"

const ChartLegend = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div
      ref={ref}
      className={cn("flex flex-wrap gap-4 text-sm", className)}
      {...props}
    />
  )
)
ChartLegend.displayName = "ChartLegend"

export {
  ChartContainer,
  ChartTitle,
  ChartDescription,
  ChartLegend,
}
