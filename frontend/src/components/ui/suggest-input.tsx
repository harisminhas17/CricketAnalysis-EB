"use client"

import * as React from "react"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Loader2, Search } from 'lucide-react'

export type SuggestOption = {
  label: string
  value: string
  subtitle?: string
  meta?: Record<string, any>
}

type SuggestInputProps = {
  value: string
  onChange: (v: string) => void
  onSelect?: (opt: SuggestOption) => void
  placeholder?: string
  fetcher: (query: string) => Promise<SuggestOption[]>
  className?: string
  inputClassName?: string
  emptyText?: string
}

export function SuggestInput({
  value,
  onChange,
  onSelect,
  placeholder = "Type to search...",
  fetcher,
  className,
  inputClassName,
  emptyText = "No suggestions",
}: SuggestInputProps) {
  const [open, setOpen] = React.useState(false)
  const [loading, setLoading] = React.useState(false)
  const [items, setItems] = React.useState<SuggestOption[]>([])
  const [highlight, setHighlight] = React.useState<number>(-1)
  const rootRef = React.useRef<HTMLDivElement>(null)
  const listRef = React.useRef<HTMLDivElement>(null)
  const latestQuery = React.useRef<string>("")
  const debounceRef = React.useRef<number | undefined>(undefined)

  React.useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (!rootRef.current) return
      if (!rootRef.current.contains(e.target as Node)) {
        setOpen(false)
        setHighlight(-1)
      }
    }
    window.addEventListener("mousedown", handler)
    return () => window.removeEventListener("mousedown", handler)
  }, [])

  const runFetch = React.useCallback(
    (q: string) => {
      if (!q || q.trim().length < 1) {
        setItems([])
        setOpen(false)
        setLoading(false)
        return
      }
      latestQuery.current = q
      setLoading(true)
      fetcher(q)
        .then((res) => {
          // Only set results if query hasn't changed mid-flight
          if (latestQuery.current === q) {
            setItems(res)
            setOpen(true)
            setHighlight(res.length ? 0 : -1)
          }
        })
        .catch(() => {
          if (latestQuery.current === q) {
            setItems([])
            setOpen(true)
            setHighlight(-1)
          }
        })
        .finally(() => {
          if (latestQuery.current === q) setLoading(false)
        })
    },
    [fetcher],
  )

  const onInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const v = e.target.value
    onChange(v)
    window.clearTimeout(debounceRef.current)
    debounceRef.current = window.setTimeout(() => runFetch(v), 250)
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (!open) return
    if (e.key === "ArrowDown") {
      e.preventDefault()
      setHighlight((h) => Math.min(h + 1, items.length - 1))
    } else if (e.key === "ArrowUp") {
      e.preventDefault()
      setHighlight((h) => Math.max(h - 1, 0))
    } else if (e.key === "Enter") {
      e.preventDefault()
      if (highlight >= 0 && items[highlight]) {
        const opt = items[highlight]
        onChange(opt.label)
        onSelect?.(opt)
        setOpen(false)
      }
    } else if (e.key === "Escape") {
      e.preventDefault()
      setOpen(false)
      setHighlight(-1)
    }
  }

  React.useEffect(() => {
    if (!listRef.current) return
    const active = listRef.current.querySelector<HTMLElement>('[data-active="true"]')
    active?.scrollIntoView({ block: "nearest" })
  }, [highlight])

  return (
    <div ref={rootRef} className={cn("relative", className)}>
      <div className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground pointer-events-none">
        <Search className="w-4 h-4" />
      </div>
      <Input
        value={value}
        onChange={onInputChange}
        onFocus={() => value && runFetch(value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        className={cn("pl-9", inputClassName)}
        aria-autocomplete="list"
        aria-expanded={open}
        aria-controls="suggestion-listbox"
        role="combobox"
      />
      {loading && (
        <div className="absolute right-2 top-1/2 -translate-y-1/2 text-muted-foreground">
          <Loader2 className="w-4 h-4 animate-spin" />
        </div>
      )}
      {open && (
        <div
          ref={listRef}
          id="suggestion-listbox"
          role="listbox"
          className="absolute z-50 mt-2 w-full rounded-md border bg-popover text-popover-foreground shadow-md max-h-64 overflow-auto"
        >
          {items.length === 0 && !loading ? (
            <div className="px-3 py-2 text-sm text-muted-foreground">{emptyText}</div>
          ) : (
            items.map((opt, idx) => (
              <button
                key={`${opt.label}-${idx}`}
                role="option"
                aria-selected={highlight === idx}
                data-active={highlight === idx ? "true" : "false"}
                onMouseEnter={() => setHighlight(idx)}
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => {
                  onChange(opt.label)
                  onSelect?.(opt)
                  setOpen(false)
                }}
                className={cn(
                  "w-full text-left px-3 py-2 text-sm hover:bg-accent hover:text-accent-foreground",
                  highlight === idx && "bg-accent text-accent-foreground",
                )}
              >
                <div className="flex items-center justify-between gap-3">
                  <span className="truncate">{opt.label}</span>
                  {opt.subtitle && <span className="text-xs text-muted-foreground truncate">{opt.subtitle}</span>}
                </div>
              </button>
            ))
          )}
        </div>
      )}
    </div>
  )
}
