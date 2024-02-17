import Link from "next/link";

import { cn } from "@/utils/utils";

export function Navbar({
  className,
  ...props
}: React.HTMLAttributes<HTMLElement>) {
  return (
    <nav
      className={cn("flex items-center space-x-4 lg:space-x-6", className)}
      {...props}
    >
      <Link
        href="/"
        className="text-xl font-medium transition-colors hover:text-primary dark:text-white flex space-x-2"
      >
        <img
          src="/simulatrex-logo-black.png"
          alt="Simulatrex.ai"
          className="w-auto h-6"
        />
        <span>Playground</span>
      </Link>
    </nav>
  );
}
