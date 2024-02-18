"use client";

import {
  Box,
  Button,
  Image,
  Grid,
  GridItem,
  HStack,
  Heading,
  Link,
  Text,
  VStack,
} from "@chakra-ui/react";
import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export default function PageAnal({ params }: { params: { doc_id: string } }) {
  const [imageUrl, setImageUrl] = useState("");
  const [pdfUrl, setPdfUrl] = useState("");
  const [quote, setQuote] = useState("");
  const [summary, setSummary] = useState("");

  useEffect(() => {
    fetchImage();
    fetchPdfUrl();
    fetchDocumentTextAndSummarize();
  }, [params.doc_id]);

  const fetchImage = async () => {
    const { data, error } = await supabase.storage
      .from("images")
      .download(`page_1-2_${params.doc_id}.jpg`);

    if (error) {
      console.error("Error fetching image:", error);
      return;
    }

    const url = URL.createObjectURL(data);
    setImageUrl(url);
  };

  const fetchPdfUrl = () => {
    const { data } = supabase.storage
      .from("pdfs")
      .getPublicUrl(`scan_${params.doc_id}.pdf`);
    setPdfUrl(data.publicUrl);
  };

  const getDocumentSummary = async (documentText: string) => {
    try {
      const response = await fetch("/api/summarize", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: documentText }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const summaryData = await response.json();
      console.log(summaryData);
      setSummary(summaryData.response); // Update state with the summary
    } catch (error) {
      console.error("Error getting document summary:", error);
    }
  };

  const fetchDocumentTextAndSummarize = async () => {
    const { data, error } = await supabase
      .from("pages")
      .select("text")
      .eq("doc_id", params.doc_id);
    if (error) {
      console.error("Error fetching document text:", error);
      return;
    }

    // Check if data exists and has entries
    if (data && data.length > 0) {
      // Concatenate all text entries to form the full document text
      const fullDocumentText = data.map((entry) => entry.text).join(" ");
      console.log(fullDocumentText)
      // Now that we have the full document text, let's get the summary
      getDocumentSummary(fullDocumentText);
    }
  };

  return (
    <VStack w={{ base: "100%", md: "50%" }} margin="auto" p={3}>
      <HStack
        justifyContent="space-between"
        w="100%"
        borderBottom="1px"
        borderColor="gray.600"
        p={3}
        mb={5}
      >
        <Heading size="2xl">Your Memories</Heading>
        <Button>Ask Questions</Button>
      </HStack>
      <Grid w="100%" templateColumns="repeat(2,1fr)" gap={6}>
        <GridItem id="summary" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">Summary</Heading>
          <Text>{summary ? summary : "Loading"}</Text>
        </GridItem>
        <GridItem id="PDF" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">PDF</Heading>
          <Link href={pdfUrl} isExternal>
            <Box pos="relative" borderRadius="lg" overflow="hidden">
              <Image
                src={imageUrl}
                alt="Doc Preview"
                maxH="200px"
                boxSize="full"
                objectFit="cover"
              />
              <Box
                pos="absolute"
                top="0"
                left="0"
                right="0"
                bottom="0"
                bg="blackAlpha.500" // Adjust the alpha value to control the darkness
                borderRadius="lg" // Match the borderRadius with the Image
              />
              <Text
                pos="absolute"
                fontWeight="bold"
                fontSize="xl"
                top="50%"
                left="50%"
                transform="translate(-50%, -50%)"
                color="white" // Ensure the text is visible on the dark background
                zIndex="1" // Make sure the text is above the overlay
              >
                See your scan
              </Text>
            </Box>
          </Link>
        </GridItem>
        <GridItem id="quote" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">Quote</Heading>
          <Text>Uwu this is a quote</Text>
        </GridItem>
        <GridItem id="stats" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">Stats</Heading>
        </GridItem>
      </Grid>
    </VStack>
  );
}
