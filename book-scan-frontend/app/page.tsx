// app/page.tsx
"use client";

import { Heading, VStack, Text, Box } from "@chakra-ui/react";
import Lottie from "lottie-react";
import bookFlipAnimation from "../public/book-flip.json";

export default function Page() {
  return (
    <VStack h="100%">
      <VStack p={5} borderBottom="1px" borderColor="gray.200" >
        <Heading size="3xl">Recollect</Heading>
        <Text fontSize="xl">Your Memories, Preserved Forever</Text>
      </VStack>
      <Box id="pdf-area" maxW="lg" maxH="lg">
        <Lottie animationData={bookFlipAnimation} loop={true} />
      </Box>
    </VStack>
  );
}
