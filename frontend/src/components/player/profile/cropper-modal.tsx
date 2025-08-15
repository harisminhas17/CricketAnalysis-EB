"use client"

import { useEffect, useRef, useState } from "react"
import { ZoomIn, ZoomOut, Move, Save, RotateCw } from 'lucide-react'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"

type CropperModalProps = {
  open: boolean
  onOpenChange: (v: boolean) => void
  imageUrl: string | null
  onCropped: (dataUrl: string) => void
  title?: string
  size?: number // output square size
}

export function CropperModal({
  open,
  onOpenChange,
  imageUrl,
  onCropped,
  title = "Crop Profile Photo",
  size = 512,
}: CropperModalProps) {
  const containerRef = useRef<HTMLDivElement>(null)
  const imgRef = useRef<HTMLImageElement>(null)

  const [scale, setScale] = useState(1)
  const [pos, setPos] = useState({ x: 0, y: 0 })
  const [isDragging, setIsDragging] = useState(false)
  const [start, setStart] = useState({ x: 0, y: 0 })
  const [imgNatural, setImgNatural] = useState({ w: 0, h: 0 })
  const [rotation, setRotation] = useState(0)

  useEffect(() => {
    if (!imageUrl) return
    const img = new Image()
    img.crossOrigin = "anonymous"
    img.onload = () => {
      setImgNatural({ w: img.width, h: img.height })
      // reset defaults for each new image
      setScale(1)
      setPos({ x: 0, y: 0 })
      setRotation(0)
    }
    img.src = imageUrl
  }, [imageUrl])

  const handlePointerDown = (e: React.PointerEvent) => {
    setIsDragging(true)
    setStart({ x: e.clientX - pos.x, y: e.clientY - pos.y })
    ;(e.target as Element).setPointerCapture?.(e.pointerId)
  }

  const handlePointerMove = (e: React.PointerEvent) => {
    if (!isDragging) return
    setPos({ x: e.clientX - start.x, y: e.clientY - start.y })
  }

  const handlePointerUp = () => setIsDragging(false)

  const cropToCanvas = () => {
    if (!imgRef.current || !containerRef.current || !imageUrl) return
    const canvas = document.createElement("canvas")
    const ctx = canvas.getContext("2d")!
    canvas.width = size
    canvas.height = size

    const containerRect = containerRef.current.getBoundingClientRect()
    const viewSize = Math.min(containerRect.width, 400) // viewport square side (approx)
    // Compute how the image maps to viewport:
    // base image fitting to viewport (cover)
    const aspectImg = imgNatural.w / imgNatural.h
    const baseW = aspectImg >= 1 ? viewSize * aspectImg : viewSize
    const baseH = aspectImg >= 1 ? viewSize : viewSize / aspectImg

    // apply scale and position offsets
    const drawW = baseW * scale
    const drawH = baseH * scale

    // center plus offset
    const centerX = size / 2 + (pos.x / viewSize) * size
    const centerY = size / 2 + (pos.y / viewSize) * size

    ctx.save()
    // Fill background transparent
    ctx.translate(centerX, centerY)
    ctx.rotate((rotation * Math.PI) / 180)
    ctx.translate(-drawW / 2, -drawH / 2)

    const img = imgRef.current
    // Draw image so that the viewport maps to canvas square
    // Scale so that viewSize maps to canvas size
    const scaleToCanvas = size / viewSize
    ctx.scale(scaleToCanvas, scaleToCanvas)
    ctx.drawImage(img, 0, 0, drawW, drawH)
    ctx.restore()

    const dataUrl = canvas.toDataURL("image/png")
    onCropped(dataUrl)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
        </DialogHeader>
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
          <div className="lg:col-span-3">
            <div
              ref={containerRef}
              className="relative mx-auto size-[340px] sm:size-[380px] bg-muted rounded-full overflow-hidden touch-none"
              onPointerDown={handlePointerDown}
              onPointerMove={handlePointerMove}
              onPointerUp={handlePointerUp}
              onPointerCancel={handlePointerUp}
              aria-label="Crop area"
              role="region"
            >
              {imageUrl ? (
                <img
                  ref={imgRef}
                  src={imageUrl || "/placeholder.svg"}
                  alt="Preview to crop"
                  className="absolute select-none"
                  style={{
                    width: "auto",
                    height: "100%",
                    left: "50%",
                    top: "50%",
                    transform: `translate(-50%,-50%) translate(${pos.x}px,${pos.y}px) scale(${scale}) rotate(${rotation}deg)`,
                    willChange: "transform",
                  }}
                  draggable={false}
                />
              ) : (
                <div className="flex size-full items-center justify-center text-sm text-muted-foreground">
                  No image
                </div>
              )}
              <div className="absolute inset-0 ring-4 ring-background/30 pointer-events-none rounded-full" />
            </div>
          </div>
          <div className="lg:col-span-2 space-y-4">
            <div>
              <div className="flex items-center justify-between text-sm mb-2">
                <span className="flex items-center gap-2">
                  <ZoomOut className="w-4 h-4" /> Zoom
                </span>
                <ZoomIn className="w-4 h-4" />
              </div>
              <Slider
                value={[scale]}
                onValueChange={(v) => setScale(v[0])}
                min={0.5}
                max={3}
                step={0.01}
              />
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" className="flex-1" onClick={() => setPos({ x: 0, y: 0 })}>
                <Move className="w-4 h-4 mr-2" />
                Center
              </Button>
              <Button variant="outline" className="flex-1" onClick={() => setRotation((r) => (r + 90) % 360)}>
                <RotateCw className="w-4 h-4 mr-2" />
                Rotate
              </Button>
            </div>
            <p className="text-xs text-muted-foreground">
              Tip: Drag to reposition. Use the slider to zoom. The circular frame represents your profile photo crop.
            </p>
          </div>
        </div>
        <DialogFooter className="mt-2">
          <DialogClose asChild>
            <Button variant="ghost">Cancel</Button>
          </DialogClose>
          <Button onClick={cropToCanvas} className="bg-[#344FA5] hover:bg-[#2A3F85]">
            <Save className="w-4 h-4 mr-2" />
            Save Photo
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  )
}
