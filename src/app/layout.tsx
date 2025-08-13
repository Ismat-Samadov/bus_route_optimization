import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL('https://pixel-art-canvas.vercel.app'),
  title: {
    default: "Pixel Art Canvas - Free Online Pixel Drawing Tool",
    template: "%s | Pixel Art Canvas"
  },
  description: "Create beautiful pixel art with our free online drawing tool. Mobile-friendly pixel canvas with color palette, grid system, and PNG export. Perfect for artists, game developers, and creative projects.",
  keywords: [
    "pixel art", "drawing tool", "canvas", "digital art", "pixel drawing", 
    "art creator", "online tool", "free", "mobile friendly", "pixel editor",
    "sprite editor", "game art", "8-bit art", "retro art", "pixel graphics"
  ],
  authors: [{ name: "Pixel Art Canvas" }],
  creator: "Pixel Art Canvas",
  publisher: "Pixel Art Canvas",
  formatDetection: {
    email: false,
    address: false,
    telephone: false,
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://pixel-art-canvas.vercel.app",
    siteName: "Pixel Art Canvas",
    title: "Pixel Art Canvas - Free Online Pixel Drawing Tool",
    description: "Create beautiful pixel art with our free online drawing tool. Mobile-friendly with color palette and PNG export.",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Pixel Art Canvas - Online Drawing Tool",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Pixel Art Canvas - Free Online Pixel Drawing Tool",
    description: "Create beautiful pixel art with our free online drawing tool. Mobile-friendly with color palette and PNG export.",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: "google-site-verification-code",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
