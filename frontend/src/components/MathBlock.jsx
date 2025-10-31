import { useEffect } from 'react';

/**
 * Renders LaTeX using MathJax.
 * @param {string} latex - The LaTeX expression to render.
 * @param {boolean} block - Whether to render as block (centered) or inline.
 */
export default function MathBlock({ latex, block = false }) {
  useEffect(() => {
    if (window.MathJax) {
      window.MathJax.typesetPromise();
    }
  }, [latex]);

  const wrapped = block ? `\

\[${latex}\\]

` : `\\(${latex}\\)`;

  return (
    <div
      className={`text-white text-lg ${block ? 'my-4 text-center' : ''}`}
      dangerouslySetInnerHTML={{ __html: wrapped }}
    />
  );
}
