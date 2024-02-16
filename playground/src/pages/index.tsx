import CodeEditor from "@/components/editor/code-editor";
import Preview from "@/components/preview/simulation-preview";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/ui/navbar";
import useRunSimulation from "@/hooks/useRunSimulation";
import { Inter } from "next/font/google";
import { useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [code, setCode] = useState("");
  const [agents, setAgents] = useState([]);
  const [currentEpoch, setCurrentEpoch] = useState(0);

  const { runSimulation } = useRunSimulation();

  // Function to handle run button click
  const handleRunClick = async () => {
    const simulationData = await runSimulation(code);
    if (simulationData) {
      setAgents(simulationData.agents);
      setCurrentEpoch(simulationData.epoch);
    }
  };

  return (
    <main className={`${inter.className} bg-white dark:bg-[#181818]`}>
      <div className="border-b">
        <div className="h-16 flex items-center px-4">
          <Navbar className="mx-6" />
          <div className="flex items-center ml-auto space-x-4">
            <p className="text-gray-700 dark:text-white">
              Current Epoch: {currentEpoch}
            </p>{" "}
            {/* Display the current epoch */}
            <Button onClick={handleRunClick}>Run</Button>
          </div>
        </div>
      </div>

      <div className="flex w-full">
        <div className="w-1/2 h-screen p-4 bg-gray-50 dark:bg-gray-700">
          <CodeEditor code={code} setCode={setCode} />
        </div>
        <div className="w-1/2 h-screen p-4">
          <Preview agents={agents} />
        </div>
      </div>
    </main>
  );
}
