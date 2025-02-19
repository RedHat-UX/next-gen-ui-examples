'use client';

import { Thread } from "@assistant-ui/react";
import { ToolFallback } from "@/components/tools/ToolFallback";
import { makeMarkdownText } from "@assistant-ui/react-markdown";

const MarkdownText = makeMarkdownText({});

export default function Home() {
    return (
        <div className="flex h-full flex-col">
            <Thread
                welcome={{
                    suggestions: [
                        {
                            //prompt: "What is Toy Story about?",
                            prompt: "Tell me details about My Name is Khan movie?",
                        }, {
                            //Who is Tom Hanks?
                            prompt: "Who is Shah Rukh Khan?"
                        }
                    ],
                }}
                assistantMessage={{
                    components: {
                        Text: MarkdownText,
                        ToolFallback
                    }
                }}
            />
        </div>
    );
}
