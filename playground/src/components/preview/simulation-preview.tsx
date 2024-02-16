import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Plane, Sphere } from "@react-three/drei";

type Agent = {
  id: number;
  position: [number, number, number];
};

type PreviewProps = {
  agents: Agent[];
};

const Preview: React.FC<PreviewProps> = ({ agents }) => {
  // Calculate the size of the environment based on the agents' positions
  const size = 10; // Example size, this can be dynamic
  const tileColor = "#EEF0F4"; // Light grey for the tiles

  return (
    <Canvas camera={{ position: [size / 2, size, size * 2], fov: 50 }}>
      <ambientLight intensity={0.8} />
      <pointLight position={[size, size, size]} />
      <OrbitControls enableRotate={false} />

      {/* Create a tilted plane to represent the environment */}
      <Plane
        rotation={[-Math.PI / 2, 0, 0]} // rotate the plane to be horizontal
        position={[size / 2, 0, size / 2]}
        args={[size, size]} // size of the plane
      >
        <meshStandardMaterial attach="material" color={tileColor} />
      </Plane>

      {/* Positioning agents on the plane */}
      {agents &&
        agents.length > 0 &&
        agents.map((agent) => (
          <Sphere
            key={agent.id}
            position={agent.position}
            args={[0.2, 32, 32]} // args for Sphere: radius, widthSegments, heightSegments
          >
            <meshStandardMaterial attach="material" color="red" />
          </Sphere>
        ))}
    </Canvas>
  );
};

export default Preview;
