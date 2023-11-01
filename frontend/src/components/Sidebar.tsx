import { EnvelopeIcon, HomeIcon } from "@heroicons/react/24/outline";

import { classNames } from "@/utils/className";

const navigation = [
  { name: "Home", href: "/", icon: HomeIcon, current: true },
  { name: "Get in touch", href: "/", icon: EnvelopeIcon, current: false },
];

type SidebarProps = {
  children: React.ReactNode;
};

export default function Sidebar({ children }: SidebarProps) {
  return (
    <div className="h-full hidden lg:z-50 lg:fixed lg:inset-y-0 lg:w-72 lg:flex lg:flex-col">
      {/* Sidebar component, swap this element with another sidebar if you like */}
      <div className="grow h-full flex flex-col gap-y-5 px-6 py-6 overflow-y-auto">
        <div className="shrink-0 h-16 flex items-center">
          <img
            className="w-auto h-12"
            src="/assets/logo.png"
            alt="Simulatrex Logo"
          />
        </div>
        <nav className="flex-1 h-full flex flex-col justify-center">
          <ul role="list" className="flex-1 flex flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map((item) => (
                  <li key={item.name}>
                    <a
                      href={item.href}
                      className={classNames(
                        item.current
                          ? "bg-gray-800 text-white"
                          : "text-gray-400 hover:text-white hover:bg-gray-800",
                        "group flex gap-x-3 p-2 text-sm font-semibold leading-6 rounded-md"
                      )}
                    >
                      <item.icon
                        className="shrink-0 w-6 h-6"
                        aria-hidden="true"
                      />
                      {item.name}
                    </a>
                  </li>
                ))}
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}
