import config_store as config
import lxml.etree as etree


def elemToDict(parent):
    ret = {}
    if parent.items(): 
      ret.update(dict(parent.items()))
    if parent.text: 
      ret['__content__'] = parent.text
    if ('List' in parent.tag):
      ret['__list__'] = []
      for element in parent:
        if element.tag is not etree.Comment:
          ret['__list__'].append(elemToDict(element))
    else:
      for element in parent:
        if element.tag is not etree.Comment:
          ret[element.tag] = elemToDict(element)
    return ret


def cusipToTicker(cusip):
  result = config.db.execute(
    "SELECT ticker FROM fails_to_deliver WHERE cusip = ?",
    (cusip, )
  )

  return result.fetchone()[0] if result.fetchone() is not None else None