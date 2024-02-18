// app/providers.tsx
"use client";
import { ChakraProvider, StyleFunctionProps } from "@chakra-ui/react";
import { extendTheme } from "@chakra-ui/react";
import { Lora, Montserrat } from "next/font/google";

const montserrat = Montserrat({ weight: '400', subsets: ['latin'] });

const lora = Lora({ weight: '400', subsets: ['latin'] });

const theme = extendTheme({
  fonts: {
    body: montserrat.style.fontFamily, // Set Montserrat as the default font for the body
    heading: lora.style.fontFamily, // Set Lora as the default font for headings
  },
  initialColorMode: "dark",
  useSystemColorMode: false,
  styles: {
    global: (props : StyleFunctionProps) => ({
      body: {
        bg: props.colorMode === "dark" ? "gray.800" : "yellow.50",
      },
    }),
  },
});

export function Providers({ children }: { children: React.ReactNode }) {
  return <ChakraProvider theme={theme}>{children}</ChakraProvider>;
}
