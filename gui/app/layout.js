import localFont from "next/font/local";
import "./globals.css";

const klavikaMedium = localFont({
  src: "./fonts/BAMKlavika-Medium.ttf",
  variable: "--font-klavika-medium",
  weight: "100 900",
});
const klavikaLight = localFont({
  src: "./fonts/BAMKlavika-Light.ttf",
  variable: "--font-klavika-light",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata = {
  title: "BAM Data Store",
  description: "Web of the BAM Data Store project.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className={`${klavikaMedium.variable} ${klavikaLight.variable} ${geistMono.variable}`}>
        {children}
      </body>
    </html>
  );
}
