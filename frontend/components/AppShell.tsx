"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { ReactNode, useState } from "react";
import {
  Compass,
  Map,
  MessageCircle,
  BookOpen,
  Settings2,
  Sun,
  Moon,
  Menu,
  X,
} from "lucide-react";
import { useTheme } from "@/components/ThemeProvider";

/** Inline Cairn logo mark — stacked stones with teal summit */
function CairnLogo({ size = 28 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" aria-label="Cairn logo">
      <ellipse cx="32" cy="54" rx="26" ry="9" fill="currentColor" opacity="0.2" />
      <ellipse cx="32" cy="51" rx="24" ry="8" fill="currentColor" opacity="0.35" />
      <ellipse cx="32" cy="36" rx="18" ry="7" fill="currentColor" opacity="0.2" />
      <ellipse cx="32" cy="34" rx="16" ry="6" fill="currentColor" opacity="0.35" />
      <ellipse cx="32" cy="22" rx="12" ry="5.5" fill="currentColor" opacity="0.2" />
      <ellipse cx="32" cy="20" rx="10" ry="4.5" fill="currentColor" opacity="0.35" />
      <ellipse cx="32" cy="11" rx="7" ry="3.5" fill="#0D9488" />
      <ellipse cx="32" cy="10" rx="5.5" ry="2.5" fill="#14B8A6" />
      <ellipse cx="32" cy="9.5" rx="3" ry="1.2" fill="#5EEAD4" opacity="0.5" />
    </svg>
  );
}

const navigation = [
  { href: "/", label: "Dashboard", icon: Compass },
  { href: "/maps", label: "Atlas Maps", icon: Map },
  { href: "/chat", label: "AI Chat", icon: MessageCircle },
  { href: "/docs", label: "Field Guide", icon: BookOpen },
  { href: "/control-room", label: "Control Room", icon: Settings2 },
];

export function AppShell({ children }: { children: ReactNode }) {
  const { theme, toggle } = useTheme();
  const pathname = usePathname();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="flex min-h-screen">
      {/* ── Sidebar ── */}
      <aside
        className={`
          fixed inset-y-0 left-0 z-40 flex w-64 flex-col border-r border-border
          bg-surface-1 transition-transform duration-300
          lg:translate-x-0
          ${mobileOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-6 py-6">
          <div className="flex h-9 w-9 items-center justify-center text-brand-500">
            <CairnLogo size={32} />
          </div>
          <div>
            <p className="text-sm font-bold tracking-wide text-content">CAIRN</p>
            <p className="text-[11px] text-content-tertiary">Offline knowledge base</p>
          </div>
        </div>

        {/* Nav */}
        <nav className="mt-2 flex-1 space-y-1 px-3">
          {navigation.map((item) => {
            const active = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
            const Icon = item.icon;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className={`
                  group flex items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium
                  transition-all duration-200
                  ${
                    active
                      ? "bg-brand-500/10 text-brand-500 dark:bg-brand-400/10 dark:text-brand-400"
                      : "text-content-secondary hover:bg-surface-2 hover:text-content"
                  }
                `}
              >
                <Icon
                  size={18}
                  strokeWidth={active ? 2.2 : 1.8}
                  className={`transition-colors ${active ? "text-brand-500 dark:text-brand-400" : "text-content-tertiary group-hover:text-content-secondary"}`}
                />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Theme toggle */}
        <div className="border-t border-border px-3 py-4">
          <button
            type="button"
            onClick={toggle}
            className="flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-[13px] font-medium text-content-secondary transition hover:bg-surface-2 hover:text-content"
          >
            {theme === "dark" ? <Sun size={18} strokeWidth={1.8} /> : <Moon size={18} strokeWidth={1.8} />}
            {theme === "dark" ? "Light Mode" : "Dark Mode"}
          </button>
        </div>
      </aside>

      {/* ── Mobile overlay ── */}
      {mobileOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/40 backdrop-blur-sm lg:hidden"
          onClick={() => setMobileOpen(false)}
        />
      )}

      {/* ── Main content ── */}
      <div className="flex flex-1 flex-col lg:pl-64">
        {/* Mobile header */}
        <header className="sticky top-0 z-20 flex items-center justify-between border-b border-border bg-surface-1/80 px-4 py-3 backdrop-blur-xl lg:hidden">
          <button
            type="button"
            onClick={() => setMobileOpen(true)}
            className="rounded-lg p-2 text-content-secondary hover:bg-surface-2 hover:text-content"
          >
            <Menu size={20} />
          </button>
          <div className="flex items-center gap-2 text-brand-500">
            <CairnLogo size={22} />
            <span className="text-sm font-bold tracking-wide text-content">CAIRN</span>
          </div>
          <button
            type="button"
            onClick={toggle}
            className="rounded-lg p-2 text-content-secondary hover:bg-surface-2 hover:text-content"
          >
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </header>

        {/* Desktop top bar */}
        <header className="sticky top-0 z-20 hidden items-center justify-between border-b border-border-subtle bg-surface-0/80 px-8 py-4 backdrop-blur-xl lg:flex">
          <div>
            <h1 className="text-xl font-semibold text-content">
              {navigation.find((n) => n.href === pathname || (n.href !== "/" && pathname.startsWith(n.href)))?.label ?? "Cairn"}
            </h1>
          </div>
          <div className="flex items-center gap-2">
            <span className="rounded-full bg-accent-600/10 px-3 py-1 text-xs font-medium text-accent-600 dark:text-accent-400">
              Local-first
            </span>
          </div>
        </header>

        <main className="flex-1 px-4 py-6 lg:px-8">{children}</main>
      </div>
    </div>
  );
}
