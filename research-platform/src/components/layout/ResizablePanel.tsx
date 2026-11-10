'use client';

import React, { useEffect, useRef, useState } from 'react';
import { ChevronLeft, ChevronRight, Files, MessageSquare } from 'lucide-react';

interface ResizablePanelProps {
  initialWidth: number; minWidth?: number; maxWidth?: number; side: 'left' | 'right';
  children: React.ReactNode; title?: string; count?: number; collapsible?: boolean;
}

export function ResizablePanel({ initialWidth, minWidth = 200, maxWidth = 500, side, children, title, count, collapsible = true }: ResizablePanelProps) {
  const [width, setWidth] = useState(Math.min(maxWidth, Math.max(minWidth, initialWidth)));
  const [collapsed, setCollapsed] = useState(false);
  const [dragging, setDragging] = useState(false);
  const start = useRef({ x: 0, width });
  const PanelIcon = side === 'left' ? Files : MessageSquare;
  const CollapseIcon = side === 'left' ? ChevronLeft : ChevronRight;
  const ExpandIcon = side === 'left' ? ChevronRight : ChevronLeft;

  useEffect(() => {
    document.body.classList.toggle('is-panel-resizing', dragging);
    return () => document.body.classList.remove('is-panel-resizing');
  }, [dragging]);

  const splitter = (
    <div className={`splitter ${dragging ? 'splitter--active' : ''}`} role="separator" aria-orientation="vertical"
      aria-label={`Resize ${title || side} panel`}
      onPointerDown={(event) => { event.preventDefault(); event.currentTarget.setPointerCapture(event.pointerId); start.current = { x: event.clientX, width }; setDragging(true); }}
      onPointerMove={(event) => { if (!dragging) return; const delta = side === 'left' ? event.clientX - start.current.x : start.current.x - event.clientX; setWidth(Math.min(maxWidth, Math.max(minWidth, start.current.width + delta))); }}
      onPointerUp={() => setDragging(false)} onPointerCancel={() => setDragging(false)} />
  );

  return <div className={`resizable-panel-shell resizable-panel-shell--${side}`} style={{ width: collapsed ? 32 : width }}>
    {side === 'right' && splitter}
    {collapsed ? <button className="panel-rail" onClick={() => setCollapsed(false)} title={`Expand ${title || side} panel`} aria-label={`Expand ${title || side} panel`}>
      <ExpandIcon size={16}/><PanelIcon size={15}/><span className="panel-rail__title">{title || (side === 'left' ? 'Artifacts' : 'Comments')}</span>
      {typeof count === 'number' && <span className="panel-rail__count">{count}</span>}
    </button> : <div className="resizable-panel">
      {collapsible && <button className={`panel-collapse panel-collapse--${side}`} onClick={() => setCollapsed(true)} title={`Collapse ${title || side} panel`} aria-label={`Collapse ${title || side} panel`}><CollapseIcon size={15}/></button>}
      {children}
    </div>}
    {side === 'left' && splitter}
  </div>;
}