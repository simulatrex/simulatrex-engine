import CodeEditor from "@/components/editor/code-editor";
import Preview from "@/components/preview/simulation-preview";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/ui/navbar";
import { Progress } from "@/components/ui/progress";
import useSimulation from "@/hooks/useRunSimulation";
import { Inter } from "next/font/google";
import { useEffect, useState } from "react";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [code, setCode] = useState("");
  const [agents, setAgents] = useState([]);
  const [currentEpoch, setCurrentEpoch] = useState(0);
  const [currentProgress, setCurrentProgress] = useState(0);
  const [simulationData, setSimulationData] = useState(null);

  const { runSimulation, cancelSimulation } = useSimulation();

  // Function to handle run button click
  const handleRunClick = async () => {
    const _simulationData = await runSimulation(code);
    if (_simulationData) {
      setAgents(_simulationData.agents);
      setCurrentEpoch(_simulationData.epoch);
      setSimulationData(_simulationData);
    }
  };

  useEffect(() => {
    try {
      const eventSource = new EventSource(
        "http://localhost:8000/api/v1/simulation/stream"
      );
      eventSource.onmessage = function (event) {
        const data = JSON.parse(event.data);
        setCurrentProgress(data.progress);
      };
      return () => {
        eventSource.close();
      };
    } catch (error) {
      console.error("EventSource failed:", error);

      return () => {};
    }
  }, []);

  return (
    <main className={`${inter.className} bg-white dark:bg-[#181818]`}>
      <div className="border-b">
        <div className="h-16 flex items-center px-4">
          <Navbar className="mx-6" />
          <div className="flex items-center space-x-4 ml-auto">
            <p className="text-gray-700 dark:text-white break-none w-auto">
              Epoch: {currentEpoch}
            </p>
            <Progress value={currentProgress} className="w-16" />

            <Button onClick={handleRunClick}>Run</Button>
            <Button onClick={cancelSimulation}>Cancel Simulation</Button>
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
