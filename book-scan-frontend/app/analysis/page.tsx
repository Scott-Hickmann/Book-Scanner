"use client";
import {
  Button,
  HStack,
  Heading,
  VStack,
  UnorderedList,
  ListItem,
  Link,
} from "@chakra-ui/react";
import { createClient } from "@supabase/supabase-js";
import { useEffect, useState } from "react";
import NextLink from "next/link"; // Import Next.js Link component for client-side transitions
import { format } from 'date-fns'; // Import format function from date-fns for formatting timestamps

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// Define a TypeScript interface for document data
interface DocData {
  doc_id: string;
  timestamp: string; // Assuming timestamp is a string, adjust based on your actual data type
}

export default function Page() {
  const [docList, setDocList] = useState<DocData[]>([]);

  useEffect(() => {
    const fetchDocs = async () => {
      let { data: pdfs, error } = await supabase
        .from("pdfs")
        .select("doc_id, timestamp"); // Select both doc_id and timestamp

      if (error) {
        console.error("Error fetching documents:", error);
        return;
      }

      if (pdfs) {
        // Map pdfs to include both doc_id and timestamp
        const docData = pdfs.map((pdf) => ({
          doc_id: pdf.doc_id,
          timestamp: pdf.timestamp,
        }));
        setDocList(docData);
      }
    };

    fetchDocs();
  }, []);

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
        <Heading size="2xl">Your Documents</Heading>
        <Button>Ask Questions</Button>
      </HStack>
      <UnorderedList styleType="none" w="full">
        {docList.map((doc, index) => (
          <ListItem key={index} mb={3}>
            <NextLink href={`/analysis/${doc.doc_id}`} passHref>
              <Link>
                <Button w="full" justifyContent="flex-start">
                  {`Document ${index + 1} - Created on ${format(new Date(doc.timestamp), 'PPPpp')}`} {/* Format the timestamp */}
                </Button>
              </Link>
            </NextLink>
          </ListItem>
        ))}
      </UnorderedList>
    </VStack>
  );
}
