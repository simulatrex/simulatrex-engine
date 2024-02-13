import React from "react";
import { Canvas } from "@react-three/fiber";
import { Box } from "@react-three/drei";

const Preview = ({
  agents,
}: {
  agents: { x: number; y: number; z: number }[];
}) => {
  return (
    <Canvas>
      {agents.map((agent, index) => (
        <Box key={index} position={[0, 0, 0]}>
          <meshStandardMaterial attach="material" color="hotpink" />
        </Box>
      ))}
    </Canvas>
  );
};

export default Preview;
