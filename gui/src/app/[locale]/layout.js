
import { ThemeProvider } from "./components/context/ThemeContext";
import localFont from "next/font/local";
import "./globals.css";
import { NextIntlClientProvider } from 'next-intl';
import { getMessages } from 'next-intl/server';
import { routing } from '../../i18n/routing';

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

// Fallback UI for unsupported languages
function LanguageNotSupported() {
  return (
    <html lang="en">
      <body className={`${klavikaMedium.variable} ${klavikaLight.variable} ${geistMono.variable}`}>
        <h1>Language not supported</h1>
        <p>
          The selected language is not supported. Please go back and choose a
          valid language.
        </p>
      </body>
    </html>
  );
};

export default async function LocaleLayout({ children, params}) {
  const { locale } = await params

  // Ensure that the incoming `locale` is valid
  if (!routing.locales.includes(locale)) {
    return <LanguageNotSupported />;
  }

  // Providing all messages to the client
  // side is the easiest way to get started
  const messages = await getMessages();

  return (
    <html lang={locale}>
      <body className={`${klavikaMedium.variable} ${klavikaLight.variable} ${geistMono.variable}`}>
        <ThemeProvider>
          <NextIntlClientProvider messages={messages}>
            {children}
          </NextIntlClientProvider>
        </ThemeProvider>
      </body>
    </html>
  );
}