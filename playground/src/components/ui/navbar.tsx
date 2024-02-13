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
        href="/app/dashboard"
        className="text-sm font-medium transition-colors hover:text-primary"
      >
        Dashboard
      </Link>
      <Link
        href="/app/search/investors"
        className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
      >
        Investor Search
      </Link>
      <Link
        href="/app/knowledge-base"
        className="text-sm font-medium text-muted-foreground transition-colors hover:text-primary"
      >
        Knowledge Base
      </Link>
    </nav>
  );
}
