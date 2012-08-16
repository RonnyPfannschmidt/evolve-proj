class TableWriter
  constructor: (@send_one, @items, @discriminate) ->
    @buffers = new Array(@items.length)
    for i in [0..@items.length]
      @buffers[i] = new Array()

  make_header: (maker) ->
    for item in @items
      maker @sendfunc(item), item

  make_footer: (maker) ->
    for item in @items
      maker @sendfunc(item)

  sendfunc: (val) ->
    if val == @items[0]
      @send_one
    else
      index = @items.indexOf(val)
      (data) =>
        @buffers[index].push(data)
        return

  make_rows: (getRow, maker) ->
    lasts = for _ in @items
      {}
    while row = getRow()
      val = @discriminate(row)
      index = @items.indexOf(val)
      lasts[index] = maker @sendfunc(val), row, lasts[index]

  finalize: () ->
    for buffer in @buffers
      buffer.forEach @send_one
    return

exports.TableWriter = TableWriter
