import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Vestaboard Vote",
  description: "Cast your vote — it shows up on the Vestaboard!",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, fontFamily: "system-ui, sans-serif", background: "#111", color: "#fff" }}>
        {children}
      </body>
    </html>
  );
}
