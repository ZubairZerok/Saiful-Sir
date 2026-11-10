declare module 'mammoth' {
  export interface Result {
    value: string;
    messages: Array<{
      type: string;
      message: string;
    }>;
  }
  export interface Options {
    styleMap?: string | string[];
    includeDefaultStyleMap?: boolean;
    convertImage?: unknown;
  }
  export const images: {
    imgElement: (fn: (image: unknown) => Promise<{ src: string }>) => unknown;
  };
  export function convertToHtml(
    input: { arrayBuffer?: ArrayBuffer; buffer?: Buffer; path?: string },
    options?: Options
  ): Promise<Result>;
  export function extractRawText(
    input: { arrayBuffer?: ArrayBuffer; buffer?: Buffer; path?: string }
  ): Promise<Result>;
}
