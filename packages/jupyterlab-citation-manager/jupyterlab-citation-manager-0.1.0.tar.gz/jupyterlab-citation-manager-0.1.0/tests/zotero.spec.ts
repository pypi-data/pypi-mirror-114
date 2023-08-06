import 'jest';

import { parseLinks } from '../src/zotero';

describe('parseLinks', () => {
  it('works for second query', () => {
    const links = parseLinks(
      '<https://api.zotero.org/users/5228248/items?format=csljson>; rel="first", <https://api.zotero.org/users/5228248/items?format=csljson>; rel="prev", <https://api.zotero.org/users/5228248/items?format=csljson&start=50>; rel="next", <https://api.zotero.org/users/5228248/items?format=csljson&start=1525>; rel="last", <https://www.zotero.org/users/5228248/items>; rel="alternate"'
    );
    expect(links.get('first')).toBe(
      'https://api.zotero.org/users/5228248/items?format=csljson'
    );
    expect(links.get('prev')).toBe(
      'https://api.zotero.org/users/5228248/items?format=csljson'
    );
    expect(links.get('next')).toBe(
      'https://api.zotero.org/users/5228248/items?format=csljson&start=50'
    );
    expect(links.get('last')).toBe(
      'https://api.zotero.org/users/5228248/items?format=csljson&start=1525'
    );
    expect(links.get('alternate')).toBe(
      'https://www.zotero.org/users/5228248/items'
    );
  });
});
