/**
 * Mathematical Expression Renderer for Biochemical Equations
 * Handles complex chemical formulas, Greek letters, reaction arrows, and LaTeX-style syntax
 */

class MathRenderer {
    constructor() {
        this.greekLetters = {
            'alpha': 'α', 'beta': 'β', 'gamma': 'γ', 'delta': 'δ', 'epsilon': 'ε',
            'zeta': 'ζ', 'eta': 'η', 'theta': 'θ', 'iota': 'ι', 'kappa': 'κ',
            'lambda': 'λ', 'mu': 'μ', 'nu': 'ν', 'xi': 'ξ', 'omicron': 'ο',
            'pi': 'π', 'rho': 'ρ', 'sigma': 'σ', 'tau': 'τ', 'upsilon': 'υ',
            'phi': 'φ', 'chi': 'χ', 'psi': 'ψ', 'omega': 'ω',
            'Alpha': 'Α', 'Beta': 'Β', 'Gamma': 'Γ', 'Delta': 'Δ', 'Epsilon': 'Ε',
            'Zeta': 'Ζ', 'Eta': 'Η', 'Theta': 'Θ', 'Iota': 'Ι', 'Kappa': 'Κ',
            'Lambda': 'Λ', 'Mu': 'Μ', 'Nu': 'Ν', 'Xi': 'Ξ', 'Omicron': 'Ο',
            'Pi': 'Π', 'Rho': 'Ρ', 'Sigma': 'Σ', 'Tau': 'Τ', 'Upsilon': 'Υ',
            'Phi': 'Φ', 'Chi': 'Χ', 'Psi': 'Ψ', 'Omega': 'Ω'
        };

        this.specialSymbols = {
            '->': '→', '=>': '⇒', '<->': '⇌', '<=>': '⇔',
            '<=': '⇐', '>=': '≥', '<=': '≤', '!=': '≠',
            '+-': '±', '-+': '∓', 'infinity': '∞', 'infty': '∞',
            'degree': '°', 'celsius': '℃', 'fahrenheit': '℉',
            'angstrom': 'Å', 'micro': 'μ', 'ohm': 'Ω'
        };

        this.initializeRenderer();
    }

    initializeRenderer() {
        // Create CSS styles for mathematical expressions
        const style = document.createElement('style');
        style.textContent = `
            .math-expression {
                font-family: 'Times New Roman', serif;
                line-height: 1.4;
                display: inline-block;
                vertical-align: baseline;
            }

            .math-subscript {
                font-size: 0.75em;
                vertical-align: sub;
                line-height: 0;
            }

            .math-superscript {
                font-size: 0.75em;
                vertical-align: super;
                line-height: 0;
            }

            .math-fraction {
                display: inline-block;
                vertical-align: middle;
                text-align: center;
            }

            .math-numerator {
                display: block;
                border-bottom: 1px solid #000;
                padding-bottom: 2px;
                margin-bottom: 2px;
            }

            .math-denominator {
                display: block;
                padding-top: 2px;
            }

            .math-sqrt {
                position: relative;
                display: inline-block;
                border-top: 1px solid #000;
                padding-top: 2px;
            }

            .math-sqrt::before {
                content: '√';
                position: absolute;
                left: -0.8em;
                top: -0.1em;
                font-size: 1.2em;
            }

            .chemical-formula {
                font-family: 'Arial', sans-serif;
                font-weight: normal;
            }

            .reaction-arrow {
                margin: 0 0.5em;
                font-size: 1.2em;
                vertical-align: middle;
            }

            .chemical-bracket {
                font-size: 1.1em;
                font-weight: bold;
            }

            .math-matrix {
                display: inline-block;
                vertical-align: middle;
                border-left: 1px solid #000;
                border-right: 1px solid #000;
                padding: 0.2em 0.5em;
            }

            .math-variable {
                font-style: italic;
                font-family: 'Times New Roman', serif;
            }
        `;
        document.head.appendChild(style);
    }

    /**
     * Main function to render mathematical expressions in the chat content
     */
    renderMathExpressions() {
        const chatContent = document.getElementById('chat-content');
        if (!chatContent) return;

        // Process all text nodes and elements
        this.processElement(chatContent);
    }

    processElement(element) {
        if (element.nodeType === Node.TEXT_NODE) {
            const text = element.textContent;
            const processedHTML = this.parseAndRenderMath(text);
            
            if (processedHTML !== text) {
                const wrapper = document.createElement('span');
                wrapper.innerHTML = processedHTML;
                element.parentNode.replaceChild(wrapper, element);
            }
        } else if (element.nodeType === Node.ELEMENT_NODE) {
            // Skip already processed math elements
            if (element.classList && element.classList.contains('math-expression')) {
                return;
            }

            // Process child nodes
            const children = Array.from(element.childNodes);
            children.forEach(child => this.processElement(child));
        }
    }

    /**
     * Parse and render mathematical expressions
     */
    parseAndRenderMath(text) {
        let result = text;

        // Handle LaTeX-style math expressions $...$ and $$...$$
        result = result.replace(/\$\$(.*?)\$\$/g, (match, content) => {
            return `<span class="math-expression">${this.renderMathContent(content.trim())}</span>`;
        });

        result = result.replace(/\$(.*?)\$/g, (match, content) => {
            return `<span class="math-expression">${this.renderMathContent(content.trim())}</span>`;
        });

        // Handle chemical equations and formulas outside of $ delimiters
        result = this.renderChemicalFormulas(result);
        result = this.renderGreekLetters(result);
        result = this.renderSpecialSymbols(result);

        return result;
    }

    /**
     * Render mathematical content (inside $ delimiters)
     */
    renderMathContent(content) {
        let result = content;

        // Handle fractions \frac{numerator}{denominator}
        result = result.replace(/\\frac\{([^}]+)\}\{([^}]+)\}/g, (match, num, den) => {
            return `<span class="math-fraction">
