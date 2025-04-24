import { useEffect, useState } from 'react';


export function useScroll() {
    const [scroll, setScroll] = useState(0);

    useEffect(() => {
        setScroll(window.scrollY);
        document.addEventListener('scroll', () => setScroll(window.scrollY));
        return () => document.removeEventListener('scroll', () => setScroll(window.scrollY));
    }, []);

    return scroll;
}
