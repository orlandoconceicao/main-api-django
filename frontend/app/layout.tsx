import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Software Sales",
  description: "Software Sales API Frontend",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-br">
      <body className="bg-zinc-950 text-white antialiased">
        {children}
      </body>
    </html>
  );
}