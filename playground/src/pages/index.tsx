import { Inter } from "next/font/google";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <main className={`min-h-screen ${inter.className}`}>
      <div className="flex w-full">
        <div className="flex w-1/2 h-screen p-4 bg-gray-100 dark:bg-gray-800">
          <textarea
            className="w-full h-full p-4 text-sm font-mono text-gray-800 bg-white border-none rounded-md shadow-sm focus:ring-0 dark:bg-gray-700 dark:text-gray-300"
            placeholder="Start typing your code here..."
          />
        </div>
        <div className="flex w-1/2 h-screen p-4">
          <div className="w-full h-full bg-white rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 overflow-hidden">
            <iframe className="w-full h-full" title="Preview" />
          </div>
        </div>
      </div>
    </main>
  );
}
