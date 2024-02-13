import Link from "next/link";

import { cn } from "@/lib/utils";

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
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Simulatrex Playground
      </Link>
    </nav>
  );
}
