class TableWriter
  constructor: (@send_one, @items, @discriminate) ->
    @buffers = new Array(@items.length)
    for i in [1..@items.length]
      @buffers[i] = new Array()

  make_header: (maker) ->
    for item in @items
      maker @sendfunc(item), item

  sendfunc: (val) ->
    if val == @items[0]
      @send_one
    else
      index = @items.indexOf(val)
      (data) =>
        @buffers[index].push(data)
        return

  make_rows: (getRow, maker) ->
    last = {}
    while row = getRow()
      val = @discriminate(row)
      last = maker @sendfunc(val), row, last

  finalize: () ->
    for buffer in @buffers
      buffer.forEach @send_one
    return

exports.TableWriter = TableWriter
