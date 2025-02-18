'use client'

import type { ToolResponse } from '@/lib/types';
import { ToolCallContentPartComponent } from '@assistant-ui/react';
import { CheckIcon, ChevronDownIcon, ChevronUpIcon } from 'lucide-react';
import { useState } from "react";
import { Button } from "../ui/button";
import { NextGenUIComponent } from '../NextGenUIComponent';

export const ToolFallback: ToolCallContentPartComponent = (part) => {
    const [isCollapsed, setIsCollapsed] = useState(true);
    let content: ToolResponse = part.result;
    try {
        content = JSON.parse(part.result);
    } catch (e) {
        console.log("Response is not JSON. Cannot prettify");
    }

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
        {part.result && <NextGenUIComponent markup={part.result}></NextGenUIComponent>}
      </section>
    }
</div>
  );
};