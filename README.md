The goals of this project is to make a pipeline between writing posts in Obsidian.md and publishing them through Hugo. The aim is to make this process as frictionless as possible.

## Structure of this project
- `test-files/obsidian-vault`: This directory contains the raw `.md` files that would come from Obsidian. This is a place holder for the Obsidian directory we would want to monitor for new posts. Right now it just has some files you can use to test. The files in this directory are left messy on purpose to simulate the way they would come from Obsidian.
- `test-files/hugo-content`: This is a representation of the `content` directory in a Hugo site. This would be were the content would end up after being processed by the pipeline. You can use it to verify that the pipeline is working as expected.

## Current manual process
1. Write a post in Obsidian.
2. Make a directory under `content` inside a matching subdirectory (like `notes`) for the post.
3. Copy the `.md` file from Obsidian to the new directory and rename it to `index.md`.
4. Copy the thumbnail image to the new directory. The thumbnail is defined in the `cover:` field in the front matter of the `.md` file.
5. Find any image links in the `.md` file and copy the images to the new directory.
6. Rename the image links in the `.md` file to make more sense.
7. Update the image links to center the images in the post.
8. Run Hugo command to build the site.
9. Check the site to make sure the post looks good.
10. Run an rsync command to copy the new post to the prod server.

## Future automated process
==To-Do==
Mermaid diagram of the process?

## Example Front Matter

This is an example of the front matter that I currently use. Some of the fields are specific to the theme that I'm using in Hugo, but I think most of them are useful. At a minimum, all we really need is `title`, `cover.image`, and `type`.

```yaml
---
title: "Post Title"
type: "notes"
date: 2024-02-15T20:21:22Z
lastmod: 2024-02-15T20:21:22Z
draft: true
showtoc: true
defaultTheme: auto
disableThemeToggle: false
author:
  - Author
tags:
  - Tag1
  - Tag2
summary: ""
cover:
  image: cover.jpg
  relative: true
  hidden: false
---
```

## Setting up Hugo
==To-Do==