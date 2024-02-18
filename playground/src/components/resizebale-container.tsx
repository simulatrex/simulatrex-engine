import React, { useRef, useState, useCallback, useEffect } from "react";

type ResizableContainerProps = {
  children: React.ReactNode;
  initialWidth: string; // Using percentages for relative sizing
  initialHeight: string; // Using percentages for relative sizing
  resizeDirection: "x" | "y" | "both";
  className?: string;
};

const ResizableContainer: React.FC<ResizableContainerProps> = ({
  children,
  initialWidth,
  initialHeight,
  resizeDirection,
  className,
}) => {
  const [dimensions, setDimensions] = useState({
    width: initialWidth,
    height: initialHeight,
  });
  const containerRef = useRef<HTMLDivElement>(null);

  const updateDimensions = useCallback(
    (newWidth: number, newHeight: number) => {
      setDimensions((prevDimensions) => ({
        width:
          resizeDirection === "x" || resizeDirection === "both"
            ? `${newWidth}px`
            : prevDimensions.width,
        height:
          resizeDirection === "y" || resizeDirection === "both"
            ? `${newHeight}px`
            : prevDimensions.height,
      }));
    },
    [resizeDirection]
  );

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleResize = (e: MouseEvent) => {
      const { clientX, clientY } = e;
      const { left, top, width, height } = container.getBoundingClientRect();

      let newWidth = width;
      let newHeight = height;

      if (resizeDirection === "x" || resizeDirection === "both") {
        newWidth = Math.max(100, clientX - left + 10); // 10px for the grab area
      }
      if (resizeDirection === "y" || resizeDirection === "both") {
        newHeight = Math.max(100, clientY - top + 10); // 10px for the grab area
      }

      updateDimensions(newWidth, newHeight);
    };

    const startResizing = (e: MouseEvent) => {
      e.preventDefault();
      document.addEventListener("mousemove", handleResize);
      document.addEventListener("mouseup", stopResizing);
    };

    const stopResizing = () => {
      document.removeEventListener("mousemove", handleResize);
      document.removeEventListener("mouseup", stopResizing);
    };

    container.addEventListener("mousedown", startResizing);

    return () => {
      container.removeEventListener("mousedown", startResizing);
    };
  }, [resizeDirection, updateDimensions]);

  return (
    <div
      ref={containerRef}
      className={className}
      style={{
        width: dimensions.width,
        height: dimensions.height,
        position: "relative",
        overflow: "hidden",
      }}
    >
      {React.Children.map(children, (child, index) => {
        return React.cloneElement(child as React.ReactElement, { key: index });
      })}
    </div>
  );
};

export default ResizableContainer;
