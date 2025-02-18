/* eslint-disable @typescript-eslint/no-explicit-any */
import { ThreadState, Client } from "@langchain/langgraph-sdk";
import { LangChainMessage } from "@assistant-ui/react-langgraph";

const createClient = () => {
  const apiUrl =
    process.env["NEXT_PUBLIC_LANGGRAPH_API_URL"] ||
    new URL("/api", window.location.href).href;
  return new Client({
    apiUrl,
  });
};

export const createAssistant = async (graphId: string) => {
    const client = createClient();
  return client.assistants.create({ graphId });
};

export const createThread = async () => {
  const client = createClient();
  return client.threads.create();
};

export const getThreadState = async (
  threadId: string
): Promise<ThreadState<Record<string, any>>> => {
  const client = createClient();
  return client.threads.getState(threadId);
};

export const updateState = async (
  threadId: string,
  fields: {
    newState: Record<string, any>;
    asNode?: string;
  }
) => {
  const client = createClient();
  return client.threads.updateState(threadId, {
    values: fields.newState,
    asNode: fields.asNode!,
  });
};

export const sendMessage = async (params: {
  threadId: string;
  messages: LangChainMessage[];
}) => {
  const client = createClient();

    // Ignore sending any Tool Messages to support "pause-resume" in LangGraph
    let messages = params.messages;
    if (messages && messages.length > 0) {
        messages = messages.filter(m => !(m.type === "tool"));
    }
    
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let input: Record<string, any> | null = null;
    if (messages.length > 0) input = {
        messages,
        genie: "enabled",
    };
  const config = {
    configurable: {
        summary_enabled: true,
    },
  };

  // warning because of subgraphs: true,
  // eslint-disable-next-line @typescript-eslint/ban-ts-comment
  //@ts-expect-error
  return client.runs.stream(
    params.threadId,
    process.env["NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID"]!,
    {
      input,
      config,
      streamMode: "messages",
      // WARNING. For some reason `streamSubgraphs` doesn't emit subgraph messages. But subgraphs yes - like in POC example runs :-)
      subgraphs: true,
      // streamSubgraphs: true,
    }
  );
};
