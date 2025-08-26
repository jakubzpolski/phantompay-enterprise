export function trackEvent(event: string, data: Record<string, any> = {}) {
  console.log("Analytics event:", event, data);
  // TODO: Connect to Segment, GA, or Plausible
}
