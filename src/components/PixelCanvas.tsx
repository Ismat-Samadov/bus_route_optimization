'use client';

import React, { useRef, useEffect, useState, useCallback } from 'react';

interface PixelCanvasProps {
  width?: number;
  height?: number;
  pixelSize?: number;
}

export default function PixelCanvas({ 
  width = 24, 
  height = 24, 
  pixelSize = 14 
}: PixelCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentColor, setCurrentColor] = useState('#000000');
  const [grid, setGrid] = useState<string[][]>(
    Array(height).fill(null).map(() => Array(width).fill('#ffffff'))
  );

  const colors = [
    '#000000', '#ffffff', '#ff0000', '#00ff00', '#0000ff', 
    '#ffff00', '#ff00ff', '#00ffff', '#ffa500', '#800080',
    '#ffc0cb', '#a52a2a', '#808080', '#90ee90', '#ffd700', '#ff69b4'
  ];

  const drawPixel = useCallback((x: number, y: number, color: string) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.fillStyle = color;
    ctx.fillRect(x * pixelSize, y * pixelSize, pixelSize, pixelSize);
  }, [pixelSize]);

  const redrawCanvas = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let y = 0; y < height; y++) {
      for (let x = 0; x < width; x++) {
        drawPixel(x, y, grid[y][x]);
      }
    }

    ctx.strokeStyle = '#e5e5e5';
    ctx.lineWidth = 0.5;
    for (let x = 0; x <= width; x++) {
      ctx.beginPath();
      ctx.moveTo(x * pixelSize, 0);
      ctx.lineTo(x * pixelSize, height * pixelSize);
      ctx.stroke();
    }
    for (let y = 0; y <= height; y++) {
      ctx.beginPath();
      ctx.moveTo(0, y * pixelSize);
      ctx.lineTo(width * pixelSize, y * pixelSize);
      ctx.stroke();
    }
  }, [grid, width, height, pixelSize, drawPixel]);

  useEffect(() => {
    redrawCanvas();
  }, [redrawCanvas]);

  const getPixelPosition = (event: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current;
    if (!canvas) return null;

    const rect = canvas.getBoundingClientRect();
    let clientX, clientY;

    if ('touches' in event && event.touches[0]) {
      clientX = event.touches[0].clientX;
      clientY = event.touches[0].clientY;
    } else if ('clientX' in event) {
      clientX = event.clientX;
      clientY = event.clientY;
    } else {
      return null;
    }

    const x = Math.floor((clientX - rect.left) / pixelSize);
    const y = Math.floor((clientY - rect.top) / pixelSize);

    return (x >= 0 && x < width && y >= 0 && y < height) ? { x, y } : null;
  };

  const handleStart = (event: React.MouseEvent | React.TouchEvent) => {
    event.preventDefault();
    setIsDrawing(true);
    const pos = getPixelPosition(event);
    if (pos) {
      const newGrid = [...grid];
      newGrid[pos.y][pos.x] = currentColor;
      setGrid(newGrid);
    }
  };

  const handleMove = (event: React.MouseEvent | React.TouchEvent) => {
    event.preventDefault();
    if (!isDrawing) return;
    
    const pos = getPixelPosition(event);
    if (pos) {
      const newGrid = [...grid];
      newGrid[pos.y][pos.x] = currentColor;
      setGrid(newGrid);
    }
  };

  const handleEnd = () => {
    setIsDrawing(false);
  };

  const clearCanvas = () => {
    setGrid(Array(height).fill(null).map(() => Array(width).fill('#ffffff')));
  };

  const downloadImage = () => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const link = document.createElement('a');
    link.download = 'pixel-art.png';
    link.href = canvas.toDataURL();
    link.click();
  };

  return (
    <div className="flex flex-col items-center space-y-4 p-4 max-w-4xl mx-auto">
      <div className="text-center mb-4">
        <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-gray-800 mb-2">
          Pixel Art Canvas
        </h1>
        <p className="text-gray-600 text-sm sm:text-base">
          Create pixel art by clicking and dragging on the canvas
        </p>
      </div>

      <div className="grid grid-cols-8 sm:grid-cols-16 gap-1 sm:gap-2 mb-4 p-2 bg-white rounded-lg shadow-sm">
        {colors.map((color) => (
          <button
            key={color}
            onClick={() => setCurrentColor(color)}
            className={`w-6 h-6 sm:w-8 sm:h-8 rounded border-2 transition-all hover:scale-110 active:scale-95 ${
              currentColor === color 
                ? 'border-gray-800 shadow-lg ring-2 ring-blue-400' 
                : 'border-gray-300 hover:border-gray-400'
            }`}
            style={{ backgroundColor: color }}
            title={color}
            aria-label={`Select color ${color}`}
          />
        ))}
      </div>

      <div className="relative">
        <div className="touch-none select-none overflow-auto max-w-full">
          <canvas
            ref={canvasRef}
            width={width * pixelSize}
            height={height * pixelSize}
            className="border-2 border-gray-300 shadow-lg cursor-crosshair bg-white rounded max-w-full h-auto"
            style={{ 
              maxWidth: '90vw',
              maxHeight: '60vh',
              imageRendering: 'pixelated'
            }}
            onMouseDown={handleStart}
            onMouseMove={handleMove}
            onMouseUp={handleEnd}
            onMouseLeave={handleEnd}
            onTouchStart={handleStart}
            onTouchMove={handleMove}
            onTouchEnd={handleEnd}
          />
        </div>
      </div>

      <div className="flex flex-col sm:flex-row gap-3 justify-center items-center w-full">
        <button
          onClick={clearCanvas}
          className="w-full sm:w-auto px-6 py-3 bg-red-500 text-white rounded-lg hover:bg-red-600 active:bg-red-700 transition-colors font-medium shadow-md"
        >
          Clear Canvas
        </button>
        <button
          onClick={downloadImage}
          className="w-full sm:w-auto px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 active:bg-blue-700 transition-colors font-medium shadow-md"
        >
          Download PNG
        </button>
      </div>

      <div className="text-xs sm:text-sm text-gray-500 text-center max-w-md">
        <p>Use mouse or touch to draw. Select colors from the palette above.</p>
        <p className="mt-1">Canvas: {width}×{height} pixels | 
          <span className="ml-1 text-green-600 font-medium">Mobile Optimized</span>
        </p>
      </div>
    </div>
  );
}