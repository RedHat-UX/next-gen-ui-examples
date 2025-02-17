export type ToolResponse = {
    errors?: Array<{
        code: number,
        message: string,
        hints?: string[]
    }>;
    data?: object;
}


// copied from API
export type HumanFeedback = {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    form_args?: Record<string, any>,
    approval_status?: "approved" | "rejected",
    tool_name: string,
}
type HumanFeedbackState = {
    human_feedback: HumanFeedback;
    // messages?: BaseMessage[];
}
