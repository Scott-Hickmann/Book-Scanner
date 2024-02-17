import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! });

export async function POST(request: Request) {
  const body = await request.json();
  const { text } = body;

  const summary = text /*.slice(0, 1000) + "..."*/; // only copy beginning 1000

  const chatCompletion = await openai.chat.completions.create({
    messages: [
      {
        role: "system",
        content:
          "Find the most iconic quote from this document. Return it verbatim.",
      },
      {
        role: "user",
        content: `Here is the document: ${summary}`,
      },
    ],
    model: "gpt-4-turbo-preview",
  });

    const response = chatCompletion.choices[0].message.content;
    return new Response(JSON.stringify({ response }), {
      headers: { "Content-Type": "application/json" },
    });
}
