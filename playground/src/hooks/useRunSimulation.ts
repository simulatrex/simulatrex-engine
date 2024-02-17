import { useState } from "react";

const useSimulation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runSimulation = async (code: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch("http://localhost:8000/api/v1/simulation", {
        method: "POST",
        body: JSON.stringify({ code }),
        headers: {
          "Content-Type": "application/json",
        },
      });
      setLoading(false);
      if (!response.ok) {
        throw new Error("Failed to run simulation");
      }
      return response.json();
    } catch (err: any) {
      setLoading(false);
      setError(err.message);
      return null;
    }
  };

  const cancelSimulation = async () => {
    try {
      const response = await fetch(
        "http://localhost:8000/api/v1/simulation/cancel",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      if (!response.ok) {
        throw new Error("Failed to cancel simulation");
      }
      console.log("Simulation cancelled successfully");
    } catch (error) {
      console.error("Error cancelling simulation:", error);
    }
  };

  return { runSimulation, cancelSimulation, loading, error };
};

export default useSimulation;
