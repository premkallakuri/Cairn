import { ReactNode } from "react";

export function SectionCard({
  title,
  eyebrow,
  children,
  className = "",
}: {
  title: string;
  eyebrow: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section
      className={`animate-fade-in rounded-2xl border border-border bg-surface-1 p-5 shadow-card transition-shadow duration-300 hover:shadow-card-hover ${className}`}
    >
      <div className="flex items-center gap-2">
        <span className="rounded-md bg-accent-600/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-accent-600 dark:bg-accent-500/10 dark:text-accent-400">
          {eyebrow}
        </span>
      </div>
      <h2 className="mt-2 text-lg font-semibold text-content">{title}</h2>
      <div className="mt-4">{children}</div>
    </section>
  );
}
