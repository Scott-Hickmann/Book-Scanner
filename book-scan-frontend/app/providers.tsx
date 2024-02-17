// app/providers.tsx
"use client";
import { ChakraProvider } from "@chakra-ui/react";
import { extendTheme } from "@chakra-ui/react";
import { Lora } from "next/font/google";

const nextFont = Lora({
  subsets: ["latin"],
});

const theme = extendTheme({
  fonts: {
    body: nextFont.style.fontFamily,
    heading: nextFont.style.fontFamily,
  },
  initialColorMode: "light",
  useSystemColorMode: false,
});

export function Providers({ children }: { children: React.ReactNode }) {
  return <ChakraProvider theme={theme}>{children}</ChakraProvider>;
}
