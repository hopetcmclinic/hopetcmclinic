from builder import run_tailwind, SimpleSiteCMS

if __name__ == "__main__":
    run_tailwind()

    cms = SimpleSiteCMS()
    cms.publish()
