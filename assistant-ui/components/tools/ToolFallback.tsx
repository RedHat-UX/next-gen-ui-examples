'use client'

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { updateState } from '@/lib/chatApi';
import type { ToolResponse, HumanFeedbackState } from '@/lib/types';
import { ToolCallContentPartComponent, useThreadList } from '@assistant-ui/react';
import { CheckIcon, ChevronDownIcon, ChevronUpIcon, XIcon } from 'lucide-react';
import { useState } from "react";
import { Button } from "../ui/button";
import { DangrousElement } from '../DangerousComponent';

export const ToolFallback: ToolCallContentPartComponent = (part) => {
    const [isCollapsed, setIsCollapsed] = useState(true);
    let content: ToolResponse;
    if (typeof part.result === "string" && !part.toolName.startsWith('genie')) {
        try {
            content = JSON.parse(part.result);
        } catch (e) {
            content = {
                errors: [{
                    code: 0,
                    message: e.message,
                }]
            }
        }
    } else {
        content = part.result;
    }
    // TODO: Is it right way ?
    const threadList = useThreadList();

    // list.mainThreadId();
    const handleReject = async () => {
        // https://langchain-ai.github.io/langgraph/cloud/how-tos/human_in_the_loop_edit_state/#edit-the-state
        const threadId = threadList.mainThreadId;
        const humanFeedbackState: HumanFeedbackState = {
            human_feedback: {
                tool_name: part.toolName,    // executeHumanInput consumes that
                approval_status: "rejected",
            }
        };
        // https://langchain-ai.github.io/langgraph/cloud/how-tos/human_in_the_loop_user_input/#adding-user-input-to-state

        await updateState(threadId, {
          newState: humanFeedbackState,   // send this new "toolMessage" to humanInput node
          asNode: "humanInput", // update of paused node !!!
        })
        part.addResult({});   // will continue (sends empty mesasge kinda hack - see chatApi.ts !!!)
    }

    const handleConfirm = async () => {
        // https://langchain-ai.github.io/langgraph/cloud/how-tos/human_in_the_loop_edit_state/#edit-the-state
        const threadId = threadList.mainThreadId;
        const humanFeedbackState: HumanFeedbackState = {
            human_feedback: {
                tool_name: part.toolName,    // executeHumanInput consumes that
                approval_status: "approved",
            }
        };
        // https://langchain-ai.github.io/langgraph/cloud/how-tos/human_in_the_loop_user_input/#adding-user-input-to-state

        await updateState(threadId, {
          newState: humanFeedbackState,   // send this new "toolMessage" to humanInput node
          asNode: "humanInput", // update of paused node !!!
        })
        part.addResult({});   // will continue (sends empty mesasge kinda hack - see chatApi.ts !!!)
  };

    return (
<div>
    <div className="mb-4 flex w-full flex-col gap-3 rounded-lg border py-3">
      <div className="flex items-center gap-2 px-4">
        <CheckIcon className="size-4" />
        <p className="">
          Used tool (Debug): <b>{part.toolName}</b>
        </p>
        <div className="flex-grow" />
        <Button onClick={() => setIsCollapsed(!isCollapsed)}>
          {isCollapsed ? <ChevronUpIcon /> : <ChevronDownIcon />}
        </Button>
      </div>
      {!isCollapsed && (
        <div className="flex flex-col gap-2 border-t pt-2">
          <div className="px-4">
            <pre className="whitespace-pre-wrap">Args: {part.argsText}</pre>
          </div>
          {part.result !== undefined && (
            <div className="border-t border-dashed px-4 pt-2">
              <p className="font-semibold">Result:</p>
              <pre className="whitespace-pre-wrap">
                {JSON.stringify(content, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>

    {part.toolName.startsWith('genie') && part.result && 
      <section aria-labelledby="prescriptive-ui">
        {part.result && <DangrousElement markup={part.result}></DangrousElement>}
      </section>
    }
            
    {content
        && content.errors
        // && (part.toolName === "get_product_errata" && content?.errors[0].code !== 400)
        && content?.errors[0].code !== 1000
        && (
    <div className="mb-4 flex w-full flex-col">
        <Card className="mx-auto w-full max-w-md">
            <CardHeader>
                <CardTitle className="text-2xl font-bold">
                    Error
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {content.errors.map(e => e.message)}
            </CardContent>
        </Card> 
    </div>
    )}
    {content && content.errors && content?.errors[0].code === 1000
        && (
    <div className="mb-4 flex w-full flex-col">
        <Card className="mx-auto w-full max-w-md">
            <CardHeader>
                <CardTitle className="text-2xl font-bold">
                    Confirmation
                </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
                {content.errors.map(e => e.message)}
            </CardContent>
            <CardFooter className="flex justify-end">
                <Button variant="outline" onClick={handleReject}>
                <XIcon className="mr-2 h-4 w-4" />
                Reject
                </Button>
                <Button onClick={handleConfirm}>
                <CheckIcon className="mr-2 h-4 w-4" />
                Confirm
                </Button>
            </CardFooter>
            </Card> 
    </div>
      )}
</div>
  );
};