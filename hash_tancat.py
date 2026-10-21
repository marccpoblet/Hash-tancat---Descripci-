LLIURE = "L"
OCUPAT = "O"
ESBORRAT = "B"


class MyHashMap:
    def __init__(self, cap: int = 13):
        self._table = [[None, None, LLIURE] for _ in range(cap)]
        self._n = 0

    def _hash_function(self, key: int) -> int:
        return key % len(self._table)

    def _find(self, key: int) -> int:
        M = len(self._table)
        start_slot = self._hash_function(key)

        for i in range(M):
            idx = (start_slot + i) % M
            entry = self._table[idx]
            status = entry[2]

            if status == LLIURE:
                return None
            elif status == OCUPAT and entry[0] == key:
                return idx

        return None

    def get(self, key: int) -> int:
        idx = self._find(key)
        if idx is not None:
            return self._table[idx][1]
        return -1

    def put(self, key: int, value: int) -> None:
        M = len(self._table)
        start_slot = self._hash_function(key)

        first_deleted_idx = None
        key_found_idx = None

        for i in range(M):
            idx = (start_slot + i) % M
            entry = self._table[idx]
            status = entry[2]

            if status == OCUPAT and entry[0] == key:
                key_found_idx = idx
                break
            elif status == ESBORRAT:
                if first_deleted_idx is None:
                    first_deleted_idx = idx
            elif status == LLIURE:
                break

        if key_found_idx is not None:
            self._table[key_found_idx][1] = value
        else:
            if first_deleted_idx is not None:
                target_idx = first_deleted_idx
            else:
                target_idx = (start_slot + i) % M

            self._table[target_idx] = [key, value, OCUPAT]
            self._n += 1

            if self._n > len(self._table) // 2:
                self._resize(2 * len(self._table) - 1)

    def remove(self, key: int) -> None:
        """Elimina la clau si existeix, marcant la posició com ESBORRAT."""
        idx = self._find(key)
        if idx is not None:
            self._table[idx] = [None, None, ESBORRAT]
            self._n -= 1

    def _resize(self, new_cap: int) -> None:
        """Crea una taula nova de mida new_cap i re-insereix les parelles OCUPAT."""
        old_table = self._table

        self._table = [[None, None, LLIURE] for _ in range(new_cap)]
        self._n = 0

        for entry in old_table:
            if entry[2] == OCUPAT:
                self.put(entry[0], entry[1])

    def __len__(self) -> int:
        return self._n
