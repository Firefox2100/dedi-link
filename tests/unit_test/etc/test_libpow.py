from dedi_link.etc.libpow import PowDriver


class TestPowDriver:
    def test_c_solve(self):
        nonce = 'dfe041b4f60cb54d082e542b109e392a'
        difficulty = 22

        driver = PowDriver()
        solution = driver._c_solve(nonce, difficulty)

        assert solution == 9642966

    def test_python_solve(self):
        nonce = 'dfe041b4f60cb54d082e542b109e392a'
        difficulty = 22

        driver = PowDriver()
        solution = driver._python_solve(nonce, difficulty)

        assert solution == 9642966

    def test_solve(self):
        nonce = 'dfe041b4f60cb54d082e542b109e392a'
        difficulty = 22

        driver = PowDriver()
        solution = driver.solve(nonce, difficulty)

        assert solution == 9642966

    def test_validate(self):
        nonce = 'dfe041b4f60cb54d082e542b109e392a'
        difficulty = 22
        response = 9642966

        driver = PowDriver()
        is_valid = driver.validate(nonce, difficulty, response)

        assert is_valid is True

    async def test_solve_async(self):
        nonce = 'dfe041b4f60cb54d082e542b109e392a'
        difficulty = 22

        driver = PowDriver()
        solution = await driver.solve_async(nonce, difficulty)

        assert solution == 9642966
