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
  IconButton,
} from "@chakra-ui/react";
import { ArrowBackIcon } from "@chakra-ui/icons";
import { useEffect, useState } from "react";
import { createClient } from "@supabase/supabase-js";
import ReactWordcloud from "react-wordcloud";

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// don't roast me lmao 🥵
const stopwords = [
  "a",
  "a's",
  "able",
  "about",
  "above",
  "according",
  "accordingly",
  "across",
  "actually",
  "after",
  "afterwards",
  "again",
  "against",
  "ain't",
  "all",
  "allow",
  "allows",
  "almost",
  "alone",
  "along",
  "already",
  "also",
  "although",
  "always",
  "am",
  "among",
  "amongst",
  "an",
  "and",
  "another",
  "any",
  "anybody",
  "anyhow",
  "anyone",
  "anything",
  "anyway",
  "anyways",
  "anywhere",
  "apart",
  "appear",
  "appreciate",
  "appropriate",
  "are",
  "aren't",
  "around",
  "as",
  "aside",
  "ask",
  "asking",
  "associated",
  "at",
  "available",
  "away",
  "awfully",
  "b",
  "be",
  "became",
  "because",
  "become",
  "becomes",
  "becoming",
  "been",
  "before",
  "beforehand",
  "behind",
  "being",
  "believe",
  "below",
  "beside",
  "besides",
  "best",
  "better",
  "between",
  "beyond",
  "both",
  "brief",
  "but",
  "by",
  "c",
  "c'mon",
  "c's",
  "came",
  "can",
  "can't",
  "cannot",
  "cant",
  "cause",
  "causes",
  "certain",
  "certainly",
  "changes",
  "clearly",
  "co",
  "com",
  "come",
  "comes",
  "concerning",
  "consequently",
  "consider",
  "considering",
  "contain",
  "containing",
  "contains",
  "corresponding",
  "could",
  "couldn't",
  "course",
  "currently",
  "d",
  "definitely",
  "described",
  "despite",
  "did",
  "didn't",
  "different",
  "do",
  "does",
  "doesn't",
  "doing",
  "don't",
  "done",
  "down",
  "downwards",
  "during",
  "e",
  "each",
  "edu",
  "eg",
  "eight",
  "either",
  "else",
  "elsewhere",
  "enough",
  "entirely",
  "especially",
  "et",
  "etc",
  "even",
  "ever",
  "every",
  "everybody",
  "everyone",
  "everything",
  "everywhere",
  "ex",
  "exactly",
  "example",
  "except",
  "f",
  "far",
  "few",
  "fifth",
  "first",
  "five",
  "followed",
  "following",
  "follows",
  "for",
  "former",
  "formerly",
  "forth",
  "four",
  "from",
  "further",
  "furthermore",
  "g",
  "get",
  "gets",
  "getting",
  "given",
  "gives",
  "go",
  "goes",
  "going",
  "gone",
  "got",
  "gotten",
  "greetings",
  "h",
  "had",
  "hadn't",
  "happens",
  "hardly",
  "has",
  "hasn't",
  "have",
  "haven't",
  "having",
  "he",
  "he's",
  "hello",
  "help",
  "hence",
  "her",
  "here",
  "here's",
  "hereafter",
  "hereby",
  "herein",
  "hereupon",
  "hers",
  "herself",
  "hi",
  "him",
  "himself",
  "his",
  "hither",
  "hopefully",
  "how",
  "howbeit",
  "however",
  "i",
  "i'd",
  "i'll",
  "i'm",
  "i've",
  "ie",
  "if",
  "ignored",
  "immediate",
  "in",
  "inasmuch",
  "inc",
  "indeed",
  "indicate",
  "indicated",
  "indicates",
  "inner",
  "insofar",
  "instead",
  "into",
  "inward",
  "is",
  "isn't",
  "it",
  "it'd",
  "it'll",
  "it's",
  "its",
  "itself",
  "j",
  "just",
  "k",
  "keep",
  "keeps",
  "kept",
  "know",
  "known",
  "knows",
  "l",
  "last",
  "lately",
  "later",
  "latter",
  "latterly",
  "least",
  "less",
  "lest",
  "let",
  "let's",
  "like",
  "liked",
  "likely",
  "little",
  "look",
  "looking",
  "looks",
  "ltd",
  "m",
  "mainly",
  "many",
  "may",
  "maybe",
  "me",
  "mean",
  "meanwhile",
  "merely",
  "might",
  "more",
  "moreover",
  "most",
  "mostly",
  "much",
  "must",
  "my",
  "myself",
  "n",
  "name",
  "namely",
  "nd",
  "near",
  "nearly",
  "necessary",
  "need",
  "needs",
  "neither",
  "never",
  "nevertheless",
  "new",
  "next",
  "nine",
  "no",
  "nobody",
  "non",
  "none",
  "noone",
  "nor",
  "normally",
  "not",
  "nothing",
  "novel",
  "now",
  "nowhere",
  "o",
  "obviously",
  "of",
  "off",
  "often",
  "oh",
  "ok",
  "okay",
  "old",
  "on",
  "once",
  "one",
  "ones",
  "only",
  "onto",
  "or",
  "other",
  "others",
  "otherwise",
  "ought",
  "our",
  "ours",
  "ourselves",
  "out",
  "outside",
  "over",
  "overall",
  "own",
  "p",
  "particular",
  "particularly",
  "per",
  "perhaps",
  "placed",
  "please",
  "plus",
  "possible",
  "presumably",
  "probably",
  "provides",
  "q",
  "que",
  "quite",
  "qv",
  "r",
  "rather",
  "rd",
  "re",
  "really",
  "reasonably",
  "regarding",
  "regardless",
  "regards",
  "relatively",
  "respectively",
  "right",
  "s",
  "said",
  "same",
  "saw",
  "say",
  "saying",
  "says",
  "second",
  "secondly",
  "see",
  "seeing",
  "seem",
  "seemed",
  "seeming",
  "seems",
  "seen",
  "self",
  "selves",
  "sensible",
  "sent",
  "serious",
  "seriously",
  "seven",
  "several",
  "shall",
  "she",
  "should",
  "shouldn't",
  "since",
  "six",
  "so",
  "some",
  "somebody",
  "somehow",
  "someone",
  "something",
  "sometime",
  "sometimes",
  "somewhat",
  "somewhere",
  "soon",
  "sorry",
  "specified",
  "specify",
  "specifying",
  "still",
  "sub",
  "such",
  "sup",
  "sure",
  "t",
  "t's",
  "take",
  "taken",
  "tell",
  "tends",
  "th",
  "than",
  "thank",
  "thanks",
  "thanx",
  "that",
  "that's",
  "thats",
  "the",
  "their",
  "theirs",
  "them",
  "themselves",
  "then",
  "thence",
  "there",
  "there's",
  "thereafter",
  "thereby",
  "therefore",
  "therein",
  "theres",
  "thereupon",
  "these",
  "they",
  "they'd",
  "they'll",
  "they're",
  "they've",
  "think",
  "third",
  "this",
  "thorough",
  "thoroughly",
  "those",
  "though",
  "three",
  "through",
  "throughout",
  "thru",
  "thus",
  "to",
  "together",
  "too",
  "took",
  "toward",
  "towards",
  "tried",
  "tries",
  "truly",
  "try",
  "trying",
  "twice",
  "two",
  "u",
  "un",
  "under",
  "unfortunately",
  "unless",
  "unlikely",
  "until",
  "unto",
  "up",
  "upon",
  "us",
  "use",
  "used",
  "useful",
  "uses",
  "using",
  "usually",
  "uucp",
  "v",
  "value",
  "various",
  "very",
  "via",
  "viz",
  "vs",
  "w",
  "want",
  "wants",
  "was",
  "wasn't",
  "way",
  "we",
  "we'd",
  "we'll",
  "we're",
  "we've",
  "welcome",
  "well",
  "went",
  "were",
  "weren't",
  "what",
  "what's",
  "whatever",
  "when",
  "whence",
  "whenever",
  "where",
  "where's",
  "whereafter",
  "whereas",
  "whereby",
  "wherein",
  "whereupon",
  "wherever",
  "whether",
  "which",
  "while",
  "whither",
  "who",
  "who's",
  "whoever",
  "whole",
  "whom",
  "whose",
  "why",
  "will",
  "willing",
  "wish",
  "with",
  "within",
  "without",
  "won't",
  "wonder",
  "would",
  "wouldn't",
  "x",
  "y",
  "yes",
  "yet",
  "you",
  "you'd",
  "you'll",
  "you're",
  "you've",
  "your",
  "yours",
  "yourself",
  "yourselves",
  "z",
  "zero",
];

export default function PageAnal({ params }: { params: { doc_id: string } }) {
  const [imageUrl, setImageUrl] = useState("");
  const [pdfUrl, setPdfUrl] = useState("");
  const [quote, setQuote] = useState("");
  const [summary, setSummary] = useState("");
  const [documentText, setDocumentText] = useState("");

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

  const getQuote = async (documentText: string) => {
    try {
      const response = await fetch("/api/quote", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: documentText }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const quoteData = await response.json();
      console.log(quoteData);
      setQuote(quoteData.response); // Update state with the quote
    } catch (error) {
      console.error("Error getting quote:", error);
    }
  };

  const fetchDocumentTextAndSummarize = async () => {
    const { data, error } = await supabase
      .from("texts")
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
      console.log(fullDocumentText);
      setDocumentText(fullDocumentText);
      getDocumentSummary(fullDocumentText);
      getQuote(fullDocumentText);
    }
  };

  const removeStopWords = (text: string) => {
    return text
      .split(/\s+/)
      .filter((word) => word)
      .filter((word) => !stopwords.includes(word))
      .join(" ");
  };

  return (
    <VStack w={{ base: "100%" }} margin="auto" p={3}>
      <HStack w="100%" borderBottom="1px" borderColor="gray.600" p={3} mb={5} justifyContent="space-between">
        <Heading size="2xl">Your Memories</Heading>
        <IconButton aria-label="go-back" icon={<ArrowBackIcon />} as={Link} href="/analysis"></IconButton>
      </HStack>
      <Grid w="100%" templateColumns="repeat(2,1fr)" gap={6}>
        <GridItem id="summary" border="1px solid grey" borderRadius="lg" p={2} >
          <Heading size="lg">Summary</Heading>
          <Text>{summary ? summary : "Loading"}</Text>
        </GridItem>
        <GridItem id="PDF" border="1px solid grey" borderRadius="lg" p={2}>
          <Heading size="lg">PDF</Heading>
          <Link href={`${pdfUrl}`} isExternal>
            <Box
              pos="relative"
              borderRadius="lg"
              border="1px solid darkgray"
              overflow="hidden"
            >
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
          <Text fontSize="2xl" fontStyle="italic">
            {quote}
          </Text>
        </GridItem>
        <GridItem
          id="wordcloud"
          border="1px solid grey"
          borderRadius="lg"
          p={2}
        >
          <Heading size="lg">Wordcloud</Heading>
          <Box w="100%">
            <ReactWordcloud
              words={removeStopWords(documentText)
                .split(/\s+/)
                .filter((word: any) => word)
                .map((word: any) => word.toLowerCase())
                .reduce((acc: any, word: string) => {
                  const found = acc.find((w: any) => w.text === word);
                  if (found) {
                    found.value++;
                  } else {
                    acc.push({ text: word, value: 1 });
                  }
                  return acc;
                }, [])}
              options={{
                padding: 1,
              }}
            />
          </Box>
        </GridItem>
        <GridItem
          id="transcript"
          border="1px solid grey"
          borderRadius="lg"
          p={2}
          gridColumn="1 / -1" // Add this line to span the entire width
        >
          <Heading size="lg">Transcript</Heading>
          <Text>{documentText}</Text>
        </GridItem>
      </Grid>
    </VStack>
  );
}
