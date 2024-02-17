import CodeEditor from "@/components/editor/code-editor";
import Preview from "@/components/preview/simulation-preview";
import { Button } from "@/components/ui/button";
import { Navbar } from "@/components/ui/navbar";
import { Progress } from "@/components/ui/progress";
import useSimulation from "@/hooks/useRunSimulation";
import { Inter } from "next/font/google";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  const [code, setCode] = useState("");
  const [agents, setAgents] = useState([]);
  const [currentEpoch, setCurrentEpoch] = useState(0);
  const [currentProgress, setCurrentProgress] = useState(0);
  const [simulationData, setSimulationData] = useState(null);
  const [simulationOutcome, setSimulationOutcome] = useState("");
  const [isRunning, setIsRunning] = useState(false);

  const { runSimulation, cancelSimulation } = useSimulation();

  // Function to handle run button click
  const handleRunClick = async () => {
    setIsRunning(true);
    const _simulationData = await runSimulation(code);
    if (_simulationData) {
      setAgents(_simulationData.agents);
      setCurrentEpoch(_simulationData.epoch);
      setSimulationData(_simulationData);
    }
  };

  const handleCancelClick = async () => {
    await cancelSimulation();
    setIsRunning(false);
    setSimulationData(null);
    setAgents([]);
    setCurrentEpoch(0);
    setCurrentProgress;
    setSimulationOutcome("");
  };

  useEffect(() => {
    try {
      const eventSource = new EventSource(
        "http://localhost:8000/api/v1/simulation/stream"
      );
      eventSource.onmessage = function (event) {
        console.log("event", event.data);
        const data = JSON.parse(event.data);
        setCurrentProgress(data.progress);
        setSimulationOutcome(data.logs);
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

            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 2 }}
            >
              {isRunning ? (
                <Button onClick={handleCancelClick}>Cancel Simulation</Button>
              ) : (
                <Button onClick={handleRunClick}>Run</Button>
              )}
            </motion.div>
          </div>
        </div>
      </div>

      <div className="flex w-full">
        <div className="w-1/2 h-screen p-4 bg-gray-50 dark:bg-gray-700">
          <CodeEditor code={code} setCode={setCode} key={"code-editor"} />
        </div>
        <div className="w-1/2 h-screen p-4">
          <div className="w-full h-4/5">
            <Preview agents={agents} />
          </div>
          <div className="h-1/5 mt-4 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-800 rounded-lg shadow">
            <h2 className="text-lg font-semibold mb-2">Simulation Logs:</h2>
            <p className="whitespace-pre-wrap font-mono">{simulationOutcome}</p>
          </div>
        </div>
      </div>
    </main>
  );
}
